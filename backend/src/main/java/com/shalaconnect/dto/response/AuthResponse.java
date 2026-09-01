package com.shalaconnect.dto.response;

import com.shalaconnect.model.User;
import lombok.*;

@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class AuthResponse {
    private String token;
    private String tokenType = "Bearer";
    private UserDto user;

    @Data @Builder @NoArgsConstructor @AllArgsConstructor
    public static class UserDto {
        private Long id;
        private String name;
        private String email;
        private String role;
        private String phone;
        private String profilePhoto;
        private boolean active;
        private java.time.LocalDateTime createdAt;
        private SchoolResponse.Summary school;
    }

    public static UserDto fromUser(User user) {
        UserDto dto = new UserDto();
        dto.setId(user.getId());
        dto.setName(user.getName());
        dto.setEmail(user.getEmail());
        dto.setRole(user.getRole().name());
        dto.setPhone(user.getPhone());
        dto.setProfilePhoto(user.getProfilePhoto());
        dto.setActive(user.isActive());
        dto.setCreatedAt(user.getCreatedAt());
        if (user.getSchool() != null) {
            dto.setSchool(SchoolResponse.Summary.from(user.getSchool()));
        }
        return dto;
    }
}
