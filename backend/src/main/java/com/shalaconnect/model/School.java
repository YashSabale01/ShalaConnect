package com.shalaconnect.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import lombok.*;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "schools")
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class School {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank
    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
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

    // School topper info
    private String topperName;
    private Double topperPercentage;
    private String topperClass;

    private String schoolPhoto;

    @Column(nullable = false)
    private boolean active = true;

    @OneToMany(mappedBy = "school", fetch = FetchType.LAZY)
    @Builder.Default
    private List<User> staff = new ArrayList<>();

    @OneToMany(mappedBy = "school", fetch = FetchType.LAZY)
    @Builder.Default
    private List<AttendanceRecord> attendanceRecords = new ArrayList<>();

    @Column(updatable = false)
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() { createdAt = LocalDateTime.now(); updatedAt = LocalDateTime.now(); }
    @PreUpdate
    protected void onUpdate() { updatedAt = LocalDateTime.now(); }
}
