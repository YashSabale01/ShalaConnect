package com.shalaconnect.model;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@Table(name = "attendance_records",
       uniqueConstraints = @UniqueConstraint(columnNames = {"school_id", "attendance_date"}))
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class AttendanceRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "school_id", nullable = false)
    private School school;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "submitted_by")
    private User submittedBy;

    @Column(nullable = false)
    private LocalDate attendanceDate;

    @Column(nullable = false)
    private Integer totalStudents;

    @Column(nullable = false)
    private Integer presentStudents;

    @Column(nullable = false)
    private Integer absentStudents;

    private Integer totalTeachers;
    private Integer presentTeachers;

    private String remarks;

    @Column(updatable = false)
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() { createdAt = LocalDateTime.now(); updatedAt = LocalDateTime.now(); }
    @PreUpdate
    protected void onUpdate() { updatedAt = LocalDateTime.now(); }

    public double getAttendancePercentage() {
        if (totalStudents == null || totalStudents == 0) return 0.0;
        return (presentStudents * 100.0) / totalStudents;
    }
}
