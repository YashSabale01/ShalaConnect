package com.shalaconnect.service;

import com.shalaconnect.dto.request.AttendanceRequest;
import com.shalaconnect.dto.response.AttendanceResponse;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;

public interface AttendanceService {
    AttendanceResponse submitAttendance(AttendanceRequest request, String submitterEmail);
    AttendanceResponse updateAttendance(Long id, AttendanceRequest request, String submitterEmail);
    List<AttendanceResponse> getAttendanceBySchool(Long schoolId);
    List<AttendanceResponse> getAttendanceBySchoolAndDateRange(Long schoolId, LocalDate start, LocalDate end);
    List<AttendanceResponse> getAllSchoolsAttendanceForDate(LocalDate date);
    Map<String, Object> getAttendanceSummary();
    byte[] exportMonthlyClusterAttendance(int year, int month);
}
