package com.shalaconnect.dto.request;

import jakarta.validation.constraints.*;
import lombok.Data;
import java.time.LocalDate;

public class SchoolRequest {

    @Data
    public static class Create {
        @NotBlank(message = "School name is required")
        private String name;

        @NotBlank(message = "UDISE code is required")
        private String udiseCode;

        private String address;
        private String village;
        private String taluka;
        private String district;
        private String pincode;
        private String phone;
        private String email;

        @Min(0) private Integer totalStudents;
        @Min(0) private Integer totalTeachers;
        private String topperName;
        private Double topperPercentage;
        private String topperClass;
    }

    @Data
    public static class Update {
        private String name;
        private String address;
        private String village;
        private String taluka;
        private String district;
        private String pincode;
        private String phone;
        private String email;
        @Min(0) private Integer totalStudents;
        @Min(0) private Integer totalTeachers;
        private String topperName;
        private Double topperPercentage;
        private String topperClass;
    }
}
