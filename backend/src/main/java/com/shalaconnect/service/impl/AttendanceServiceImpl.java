package com.shalaconnect.service.impl;

import com.shalaconnect.dto.request.AttendanceRequest;
import com.shalaconnect.dto.response.AttendanceResponse;
import com.shalaconnect.exception.BadRequestException;
import com.shalaconnect.exception.ResourceNotFoundException;
import com.shalaconnect.model.AttendanceRecord;
import com.shalaconnect.model.Notification;
import com.shalaconnect.model.School;
import com.shalaconnect.model.User;
import com.shalaconnect.repository.AttendanceRepository;
import com.shalaconnect.repository.NotificationRepository;
import com.shalaconnect.repository.SchoolRepository;
import com.shalaconnect.repository.UserRepository;
import com.shalaconnect.service.AttendanceService;
import lombok.RequiredArgsConstructor;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.time.LocalDate;
import java.util.*;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class AttendanceServiceImpl implements AttendanceService {

    private final AttendanceRepository attendanceRepository;
    private final SchoolRepository schoolRepository;
    private final UserRepository userRepository;
    private final NotificationRepository notificationRepository;

    @Override
    @Transactional
    public AttendanceResponse submitAttendance(AttendanceRequest request, String submitterEmail) {
        School school = schoolRepository.findById(request.getSchoolId())
            .orElseThrow(() -> new ResourceNotFoundException("School", request.getSchoolId()));

        User submitter = userRepository.findByEmailWithSchool(submitterEmail)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        if (submitter.getRole() == User.Role.HEADMASTER) {
            if (submitter.getSchool() == null || !submitter.getSchool().getId().equals(request.getSchoolId())) {
                throw new BadRequestException("You are only authorized to submit attendance for your assigned school (" +
                    (submitter.getSchool() != null ? submitter.getSchool().getName() : "No school assigned") + ")");
            }
        }

        // Check if already submitted for this date
        if (attendanceRepository.findBySchoolIdAndAttendanceDate(
                request.getSchoolId(), request.getAttendanceDate()).isPresent()) {
            throw new BadRequestException("Attendance already submitted for " +
                school.getName() + " on " + request.getAttendanceDate());
        }

        if (request.getPresentStudents() > request.getTotalStudents()) {
            throw new BadRequestException("Present students cannot exceed total students");
        }

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

        record = attendanceRepository.save(record);

        // Notify cluster admin
        final Long recId = record.getId();
        final String schoolName = school.getName();
        final double pct = record.getAttendancePercentage();
        final LocalDate attDate = record.getAttendanceDate();
        userRepository.findByRoleAndActiveTrue(User.Role.ADMIN).forEach(admin -> {
            notificationRepository.save(Notification.builder()
                .user(admin)
                .title("Attendance Submitted")
                .message(schoolName + " submitted attendance for " + attDate + " (" + Math.round(pct) + "% present)")
                .type(Notification.NotificationType.GENERAL)
                .referenceId(recId)
                .referenceType("ATTENDANCE")
                .build());
        });

        return AttendanceResponse.from(record);
    }

    @Override
    @Transactional
    public AttendanceResponse updateAttendance(Long id, AttendanceRequest request, String submitterEmail) {
        AttendanceRecord record = attendanceRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Attendance record", id));

        User submitter = userRepository.findByEmailWithSchool(submitterEmail)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        if (submitter.getRole() == User.Role.HEADMASTER) {
            if (submitter.getSchool() == null || !submitter.getSchool().getId().equals(record.getSchool().getId())) {
                throw new BadRequestException("You are only authorized to update attendance for your assigned school");
            }
        }

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

    @Override
    @Transactional(readOnly = true)
    public byte[] exportMonthlyClusterAttendance(int year, int month) {
        LocalDate start = LocalDate.of(year, month, 1);
        LocalDate end = start.withDayOfMonth(start.lengthOfMonth());

        List<School> schools = schoolRepository.findAllActiveSortedByNameWithStaff();
        List<AttendanceRecord> records = attendanceRepository.findByDateRange(start, end);

        Map<Long, List<AttendanceRecord>> bySchool = records.stream()
            .collect(Collectors.groupingBy(r -> r.getSchool().getId()));

        try (Workbook workbook = new XSSFWorkbook(); ByteArrayOutputStream out = new ByteArrayOutputStream()) {
            Sheet sheet = workbook.createSheet("Monthly Cluster Attendance");

            // Header styling
            CellStyle headerStyle = workbook.createCellStyle();
            Font headerFont = workbook.createFont();
            headerFont.setBold(true);
            headerStyle.setFont(headerFont);
            headerStyle.setFillForegroundColor(IndexedColors.GREY_25_PERCENT.getIndex());
            headerStyle.setFillPattern(FillPatternType.SOLID_FOREGROUND);
            headerStyle.setBorderBottom(BorderStyle.THIN);

            // Title row
            Row titleRow = sheet.createRow(0);
            Cell titleCell = titleRow.createCell(0);
            titleCell.setCellValue("ShalaConnect - Monthly Cluster Attendance Report (" + start.getMonth().name() + " " + year + ")");

            // Header row
            Row headerRow = sheet.createRow(2);
            String[] headers = {
                "Sr No", "School Name", "UDISE Code", "Total Students",
                "Days Reported", "Avg Attendance %", "Total Present Days", "Total Possible Days", "Compliance Status"
            };
            for (int i = 0; i < headers.length; i++) {
                Cell c = headerRow.createCell(i);
                c.setCellValue(headers[i]);
                c.setCellStyle(headerStyle);
            }

            int rowIdx = 3;
            int srNo = 1;
            for (School s : schools) {
                List<AttendanceRecord> sRecords = bySchool.getOrDefault(s.getId(), Collections.emptyList());
                double avgPct = sRecords.stream().mapToDouble(AttendanceRecord::getAttendancePercentage).average().orElse(0.0);
                int daysReported = sRecords.size();
                int totalPresent = sRecords.stream().mapToInt(AttendanceRecord::getPresentStudents).sum();
                int totalPossible = sRecords.stream().mapToInt(AttendanceRecord::getTotalStudents).sum();

                Row row = sheet.createRow(rowIdx++);
                row.createCell(0).setCellValue(srNo++);
                row.createCell(1).setCellValue(s.getName());
                row.createCell(2).setCellValue(s.getUdiseCode());
                row.createCell(3).setCellValue(s.getTotalStudents() != null ? s.getTotalStudents() : 0);
                row.createCell(4).setCellValue(daysReported);
                row.createCell(5).setCellValue(Math.round(avgPct * 10.0) / 10.0);
                row.createCell(6).setCellValue(totalPresent);
                row.createCell(7).setCellValue(totalPossible);
                row.createCell(8).setCellValue(daysReported >= 15 ? "Regular" : (daysReported > 0 ? "Partial" : "Non-Compliant"));
            }

            for (int i = 0; i < headers.length; i++) {
                sheet.autoSizeColumn(i);
            }

            workbook.write(out);
            return out.toByteArray();
        } catch (IOException e) {
            throw new BadRequestException("Failed to generate monthly attendance Excel: " + e.getMessage());
        }
    }
}
