package com.shalaconnect.controller;

import com.shalaconnect.dto.request.AuthRequest;
import com.shalaconnect.dto.response.ApiResponse;
import com.shalaconnect.dto.response.AuthResponse;
import com.shalaconnect.service.AuthService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    @PostMapping("/login")
    public ResponseEntity<ApiResponse<AuthResponse>> login(
            @Valid @RequestBody AuthRequest.Login request) {
        AuthResponse response = authService.login(request);
        return ResponseEntity.ok(ApiResponse.success("Login successful", response));
    }

    @PostMapping("/register-headmaster")
    public ResponseEntity<ApiResponse<AuthResponse.UserDto>> registerHeadmaster(
            @Valid @RequestBody AuthRequest.RegisterHeadmaster request) {
        AuthResponse.UserDto user = authService.registerHeadmaster(request);
        return ResponseEntity.ok(ApiResponse.success("Headmaster registered successfully", user));
    }

    @GetMapping("/me")
    public ResponseEntity<ApiResponse<AuthResponse.UserDto>> getCurrentUser(
            @AuthenticationPrincipal UserDetails userDetails) {
        AuthResponse.UserDto user = authService.getCurrentUser(userDetails.getUsername());
        return ResponseEntity.ok(ApiResponse.success(user));
    }

    @PostMapping("/change-password")
    public ResponseEntity<ApiResponse<Void>> changePassword(
            @AuthenticationPrincipal UserDetails userDetails,
            @Valid @RequestBody AuthRequest.ChangePassword request) {
        authService.changePassword(userDetails.getUsername(), request);
        return ResponseEntity.ok(ApiResponse.success("Password changed successfully", null));
    }
}
