package com.shalaconnect.dto.request;

import com.shalaconnect.model.Event;
import com.shalaconnect.model.Meeting;
import jakarta.validation.constraints.*;
import lombok.Data;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
public class AttendanceRequest {
    @NotNull(message = "School ID is required")
    private Long schoolId;

    @NotNull(message = "Date is required")
    private LocalDate attendanceDate;

    @NotNull @Min(0)
    private Integer totalStudents;

    @NotNull @Min(0)
    private Integer presentStudents;

    @Min(0) private Integer totalTeachers;
    @Min(0) private Integer presentTeachers;
    private String remarks;
}
