package com.shalaconnect.controller;

import com.shalaconnect.dto.response.ApiResponse;
import com.shalaconnect.dto.response.AuthResponse;
import com.shalaconnect.exception.ResourceNotFoundException;
import com.shalaconnect.model.User;
import com.shalaconnect.repository.SchoolRepository;
import com.shalaconnect.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
@PreAuthorize("hasRole('ADMIN')")
public class UserController {

    private final UserRepository userRepository;
    private final SchoolRepository schoolRepository;

    @GetMapping
    public ResponseEntity<ApiResponse<List<AuthResponse.UserDto>>> getAllUsers() {
        List<AuthResponse.UserDto> users = userRepository.findAll().stream()
            .map(AuthResponse::fromUser)
            .collect(Collectors.toList());
        return ResponseEntity.ok(ApiResponse.success(users));
    }

    @GetMapping("/headmasters")
    public ResponseEntity<ApiResponse<List<AuthResponse.UserDto>>> getAllHeadmasters() {
        List<AuthResponse.UserDto> users = userRepository.findByRoleAndActiveTrue(User.Role.HEADMASTER)
            .stream().map(AuthResponse::fromUser).collect(Collectors.toList());
        return ResponseEntity.ok(ApiResponse.success(users));
    }

    @PatchMapping("/{id}/assign-school")
    public ResponseEntity<ApiResponse<AuthResponse.UserDto>> assignSchool(
            @PathVariable Long id,
            @RequestBody Map<String, Object> body) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("User", id));
        Object schoolIdObj = body.get("schoolId");
        if (schoolIdObj == null) {
            user.setSchool(null);
        } else {
            Long schoolId = Long.valueOf(schoolIdObj.toString());
            com.shalaconnect.model.School school = schoolRepository.findById(schoolId)
                .orElseThrow(() -> new ResourceNotFoundException("School", schoolId));
            user.setSchool(school);
        }
        user = userRepository.save(user);
        return ResponseEntity.ok(ApiResponse.success("School assigned", AuthResponse.fromUser(user)));
    }

    @PatchMapping("/{id}/toggle-active")
    public ResponseEntity<ApiResponse<AuthResponse.UserDto>> toggleActive(@PathVariable Long id) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("User", id));
        user.setActive(!user.isActive());
        user = userRepository.save(user);
        return ResponseEntity.ok(ApiResponse.success(
            "User " + (user.isActive() ? "activated" : "deactivated"), AuthResponse.fromUser(user)));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<ApiResponse<Void>> deleteUser(@PathVariable Long id) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("User", id));
        user.setActive(false);
        userRepository.save(user);
        return ResponseEntity.ok(ApiResponse.success("User deactivated", null));
    }
}
