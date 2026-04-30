package com.shalaconnect.service;

import com.shalaconnect.dto.request.AuthRequest;
import com.shalaconnect.dto.response.AuthResponse;
import com.shalaconnect.model.User;

public interface AuthService {
    AuthResponse login(AuthRequest.Login request);
    AuthResponse.UserDto registerHeadmaster(AuthRequest.RegisterHeadmaster request);
    AuthResponse.UserDto getCurrentUser(String email);
    void changePassword(String email, AuthRequest.ChangePassword request);
}
