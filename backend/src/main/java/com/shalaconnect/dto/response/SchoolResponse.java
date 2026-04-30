package com.shalaconnect.dto.response;

import com.shalaconnect.model.School;
import lombok.*;
import java.time.LocalDateTime;

@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class SchoolResponse {
    private Long id;
    private String name;
    private String udiseCode;
    private String address;
    private String village;
    private String taluka;
    private String district;
    private String pincode;
    private String phone;
    private String email;
    private Integer totalStudents;
    private Integer totalTeachers;
    private String topperName;
    private Double topperPercentage;
    private String topperClass;
    private String schoolPhoto;
    private boolean active;
    private LocalDateTime createdAt;

    public static SchoolResponse from(School s) {
        return SchoolResponse.builder()
            .id(s.getId()).name(s.getName()).udiseCode(s.getUdiseCode())
            .address(s.getAddress()).village(s.getVillage()).taluka(s.getTaluka())
            .district(s.getDistrict()).pincode(s.getPincode()).phone(s.getPhone())
            .email(s.getEmail()).totalStudents(s.getTotalStudents()).totalTeachers(s.getTotalTeachers())
            .topperName(s.getTopperName()).topperPercentage(s.getTopperPercentage())
            .topperClass(s.getTopperClass()).schoolPhoto(s.getSchoolPhoto())
            .active(s.isActive()).createdAt(s.getCreatedAt()).build();
    }

    @Data @Builder @NoArgsConstructor @AllArgsConstructor
    public static class Summary {
        private Long id;
        private String name;
        private String udiseCode;
        private String village;

        public static Summary from(School s) {
            return Summary.builder()
                .id(s.getId()).name(s.getName())
                .udiseCode(s.getUdiseCode()).village(s.getVillage()).build();
        }
    }
}
