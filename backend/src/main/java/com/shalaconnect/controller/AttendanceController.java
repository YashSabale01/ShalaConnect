package com.shalaconnect.controller;

import com.shalaconnect.dto.request.AttendanceRequest;
import com.shalaconnect.dto.response.ApiResponse;
import com.shalaconnect.dto.response.AttendanceResponse;
import com.shalaconnect.service.AttendanceService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/attendance")
@RequiredArgsConstructor
public class AttendanceController {

    private final AttendanceService attendanceService;

    @PostMapping
    public ResponseEntity<ApiResponse<AttendanceResponse>> submitAttendance(
            @Valid @RequestBody AttendanceRequest request,
            @AuthenticationPrincipal UserDetails userDetails) {
        AttendanceResponse response = attendanceService.submitAttendance(request, userDetails.getUsername());
        return ResponseEntity.ok(ApiResponse.success("Attendance submitted successfully", response));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN','HEADMASTER')")
    public ResponseEntity<ApiResponse<AttendanceResponse>> updateAttendance(
            @PathVariable Long id,
            @Valid @RequestBody AttendanceRequest request,
            @AuthenticationPrincipal UserDetails userDetails) {
        AttendanceResponse response = attendanceService.updateAttendance(id, request, userDetails.getUsername());
        return ResponseEntity.ok(ApiResponse.success("Attendance updated", response));
    }

    @GetMapping("/school/{schoolId}")
    public ResponseEntity<ApiResponse<List<AttendanceResponse>>> getBySchool(
            @PathVariable Long schoolId) {
        return ResponseEntity.ok(ApiResponse.success(attendanceService.getAttendanceBySchool(schoolId)));
    }

    @GetMapping("/school/{schoolId}/range")
    public ResponseEntity<ApiResponse<List<AttendanceResponse>>> getBySchoolAndRange(
            @PathVariable Long schoolId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate start,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate end) {
        return ResponseEntity.ok(ApiResponse.success(
            attendanceService.getAttendanceBySchoolAndDateRange(schoolId, start, end)));
    }

    @GetMapping("/date/{date}")
    public ResponseEntity<ApiResponse<List<AttendanceResponse>>> getByDate(
            @PathVariable @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate date) {
        return ResponseEntity.ok(ApiResponse.success(
            attendanceService.getAllSchoolsAttendanceForDate(date)));
    }

    @GetMapping("/summary")
    public ResponseEntity<ApiResponse<Map<String, Object>>> getSummary() {
        return ResponseEntity.ok(ApiResponse.success(attendanceService.getAttendanceSummary()));
    }
}
