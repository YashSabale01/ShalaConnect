package com.shalaconnect.dto.response;

import com.shalaconnect.model.AttendanceRecord;
import lombok.*;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class AttendanceResponse {
    private Long id;
    private Long schoolId;
    private String schoolName;
    private LocalDate attendanceDate;
    private Integer totalStudents;
    private Integer presentStudents;
    private Integer absentStudents;
    private Integer totalTeachers;
    private Integer presentTeachers;
    private Double attendancePercentage;
    private String remarks;
    private String submittedByName;
    private LocalDateTime createdAt;

    public static AttendanceResponse from(AttendanceRecord r) {
        return AttendanceResponse.builder()
            .id(r.getId())
            .schoolId(r.getSchool().getId())
            .schoolName(r.getSchool().getName())
            .attendanceDate(r.getAttendanceDate())
            .totalStudents(r.getTotalStudents())
            .presentStudents(r.getPresentStudents())
            .absentStudents(r.getAbsentStudents())
            .totalTeachers(r.getTotalTeachers())
            .presentTeachers(r.getPresentTeachers())
            .attendancePercentage(r.getAttendancePercentage())
            .remarks(r.getRemarks())
            .submittedByName(r.getSubmittedBy() != null ? r.getSubmittedBy().getName() : null)
            .createdAt(r.getCreatedAt())
            .build();
    }
}
