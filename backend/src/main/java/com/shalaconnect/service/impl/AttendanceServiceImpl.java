package com.shalaconnect.service.impl;

import com.shalaconnect.dto.request.AttendanceRequest;
import com.shalaconnect.dto.response.AttendanceResponse;
import com.shalaconnect.exception.BadRequestException;
import com.shalaconnect.exception.ResourceNotFoundException;
import com.shalaconnect.model.AttendanceRecord;
import com.shalaconnect.model.School;
import com.shalaconnect.model.User;
import com.shalaconnect.repository.AttendanceRepository;
import com.shalaconnect.repository.SchoolRepository;
import com.shalaconnect.repository.UserRepository;
import com.shalaconnect.service.AttendanceService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.*;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class AttendanceServiceImpl implements AttendanceService {

    private final AttendanceRepository attendanceRepository;
    private final SchoolRepository schoolRepository;
    private final UserRepository userRepository;

    @Override
    @Transactional
    public AttendanceResponse submitAttendance(AttendanceRequest request, String submitterEmail) {
        School school = schoolRepository.findById(request.getSchoolId())
            .orElseThrow(() -> new ResourceNotFoundException("School", request.getSchoolId()));

        // Check if already submitted for this date
        if (attendanceRepository.findBySchoolIdAndAttendanceDate(
                request.getSchoolId(), request.getAttendanceDate()).isPresent()) {
            throw new BadRequestException("Attendance already submitted for " +
                school.getName() + " on " + request.getAttendanceDate());
        }

        if (request.getPresentStudents() > request.getTotalStudents()) {
            throw new BadRequestException("Present students cannot exceed total students");
        }

        User submitter = userRepository.findByEmail(submitterEmail)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        AttendanceRecord record = AttendanceRecord.builder()
            .school(school)
            .submittedBy(submitter)
            .attendanceDate(request.getAttendanceDate())
            .totalStudents(request.getTotalStudents())
            .presentStudents(request.getPresentStudents())
            .absentStudents(request.getTotalStudents() - request.getPresentStudents())
            .totalTeachers(request.getTotalTeachers())
            .presentTeachers(request.getPresentTeachers())
            .remarks(request.getRemarks())
            .build();

        return AttendanceResponse.from(attendanceRepository.save(record));
    }

    @Override
    @Transactional
    public AttendanceResponse updateAttendance(Long id, AttendanceRequest request, String submitterEmail) {
        AttendanceRecord record = attendanceRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Attendance record", id));

        if (request.getPresentStudents() > request.getTotalStudents()) {
            throw new BadRequestException("Present students cannot exceed total students");
        }

        record.setTotalStudents(request.getTotalStudents());
        record.setPresentStudents(request.getPresentStudents());
        record.setAbsentStudents(request.getTotalStudents() - request.getPresentStudents());
        record.setTotalTeachers(request.getTotalTeachers());
        record.setPresentTeachers(request.getPresentTeachers());
        record.setRemarks(request.getRemarks());

        return AttendanceResponse.from(attendanceRepository.save(record));
    }

    @Override
    @Transactional(readOnly = true)
    public List<AttendanceResponse> getAttendanceBySchool(Long schoolId) {
        return attendanceRepository.findBySchoolIdOrderByAttendanceDateDesc(schoolId).stream()
            .map(AttendanceResponse::from)
            .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<AttendanceResponse> getAttendanceBySchoolAndDateRange(
            Long schoolId, LocalDate start, LocalDate end) {
        return attendanceRepository
            .findBySchoolIdAndAttendanceDateBetweenOrderByAttendanceDateAsc(schoolId, start, end)
            .stream().map(AttendanceResponse::from).collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<AttendanceResponse> getAllSchoolsAttendanceForDate(LocalDate date) {
        return attendanceRepository.findByAttendanceDate(date).stream()
            .map(AttendanceResponse::from)
            .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public Map<String, Object> getAttendanceSummary() {
        LocalDate today = LocalDate.now();
        LocalDate monthStart = today.withDayOfMonth(1);

        List<AttendanceRecord> todayRecords = attendanceRepository.findByAttendanceDate(today);
        List<AttendanceRecord> monthRecords = attendanceRepository.findByDateRange(monthStart, today);

        long totalSchools = schoolRepository.findByActiveTrue().size();
        long submittedToday = todayRecords.size();

        double avgAttendanceToday = todayRecords.stream()
            .mapToDouble(AttendanceRecord::getAttendancePercentage).average().orElse(0);

        double avgAttendanceMonth = monthRecords.stream()
            .mapToDouble(AttendanceRecord::getAttendancePercentage).average().orElse(0);

        Map<String, Object> summary = new LinkedHashMap<>();
        summary.put("totalSchools", totalSchools);
        summary.put("submittedToday", submittedToday);
        summary.put("pendingToday", totalSchools - submittedToday);
        summary.put("avgAttendanceToday", Math.round(avgAttendanceToday * 10.0) / 10.0);
        summary.put("avgAttendanceMonth", Math.round(avgAttendanceMonth * 10.0) / 10.0);
        summary.put("todayRecords", todayRecords.stream().map(AttendanceResponse::from).collect(Collectors.toList()));
        return summary;
    }
}
