package com.shalaconnect.service.impl;

import com.shalaconnect.dto.request.AuthRequest;
import com.shalaconnect.dto.response.AuthResponse;
import com.shalaconnect.exception.BadRequestException;
import com.shalaconnect.exception.ResourceNotFoundException;
import com.shalaconnect.model.School;
import com.shalaconnect.model.User;
import com.shalaconnect.repository.SchoolRepository;
import com.shalaconnect.repository.UserRepository;
import com.shalaconnect.security.JwtUtil;
import com.shalaconnect.service.AuthService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService {

    private final AuthenticationManager authenticationManager;
    private final UserRepository userRepository;
    private final SchoolRepository schoolRepository;
    private final JwtUtil jwtUtil;
    private final PasswordEncoder passwordEncoder;

    @Override
    public AuthResponse login(AuthRequest.Login request) {
        Authentication auth = authenticationManager.authenticate(
            new UsernamePasswordAuthenticationToken(request.getEmail(), request.getPassword())
        );
        User user = (User) auth.getPrincipal();
        // Re-fetch with school eagerly loaded to avoid LazyInitializationException
        user = userRepository.findByEmailWithSchool(user.getEmail()).orElse(user);
        String token = jwtUtil.generateToken(user);
        return AuthResponse.builder()
            .token(token)
            .tokenType("Bearer")
            .user(AuthResponse.fromUser(user))
            .build();
    }

    @Override
    @Transactional
    public AuthResponse.UserDto registerHeadmaster(AuthRequest.RegisterHeadmaster request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new BadRequestException("Email already registered: " + request.getEmail());
        }

        School school = null;
        if (request.getSchoolId() != null) {
            school = schoolRepository.findById(request.getSchoolId())
                .orElseThrow(() -> new ResourceNotFoundException("School", request.getSchoolId()));
        }

        User user = User.builder()
            .name(request.getName())
            .email(request.getEmail())
            .password(passwordEncoder.encode(request.getPassword()))
            .role(User.Role.HEADMASTER)
            .phone(request.getPhone())
            .school(school)
            .active(true)
            .build();

        user = userRepository.save(user);
        return AuthResponse.fromUser(user);
    }

    @Override
    @Transactional(readOnly = true)
    public AuthResponse.UserDto getCurrentUser(String email) {
        User user = userRepository.findByEmail(email)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));
        return AuthResponse.fromUser(user);
    }

    @Override
    @Transactional
    public void changePassword(String email, AuthRequest.ChangePassword request) {
        User user = userRepository.findByEmail(email)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        if (!passwordEncoder.matches(request.getCurrentPassword(), user.getPassword())) {
            throw new BadRequestException("Current password is incorrect");
        }

        user.setPassword(passwordEncoder.encode(request.getNewPassword()));
        userRepository.save(user);
    }
}
