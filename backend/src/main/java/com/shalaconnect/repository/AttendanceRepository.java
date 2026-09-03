package com.shalaconnect.repository;

import com.shalaconnect.model.AttendanceRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Repository
public interface AttendanceRepository extends JpaRepository<AttendanceRecord, Long> {

    @Query("SELECT a FROM AttendanceRecord a LEFT JOIN FETCH a.school LEFT JOIN FETCH a.submittedBy WHERE a.school.id = :schoolId ORDER BY a.attendanceDate DESC")
    List<AttendanceRecord> findBySchoolIdOrderByAttendanceDateDesc(@Param("schoolId") Long schoolId);

    Optional<AttendanceRecord> findBySchoolIdAndAttendanceDate(Long schoolId, LocalDate date);

    @Query("SELECT a FROM AttendanceRecord a LEFT JOIN FETCH a.school LEFT JOIN FETCH a.submittedBy WHERE a.school.id = :schoolId AND a.attendanceDate BETWEEN :start AND :end ORDER BY a.attendanceDate ASC")
    List<AttendanceRecord> findBySchoolIdAndAttendanceDateBetweenOrderByAttendanceDateAsc(
        @Param("schoolId") Long schoolId, @Param("start") LocalDate start, @Param("end") LocalDate end);

    @Query("SELECT a FROM AttendanceRecord a LEFT JOIN FETCH a.school LEFT JOIN FETCH a.submittedBy WHERE a.attendanceDate = :date ORDER BY a.school.name ASC")
    List<AttendanceRecord> findByAttendanceDate(@Param("date") LocalDate date);

    @Query("SELECT a FROM AttendanceRecord a LEFT JOIN FETCH a.school LEFT JOIN FETCH a.submittedBy WHERE a.attendanceDate BETWEEN :start AND :end ORDER BY a.attendanceDate ASC")
    List<AttendanceRecord> findByDateRange(@Param("start") LocalDate start, @Param("end") LocalDate end);

    @Query("SELECT AVG(a.presentStudents * 100.0 / a.totalStudents) FROM AttendanceRecord a WHERE a.school.id = :schoolId AND a.attendanceDate BETWEEN :start AND :end")
    Double findAverageAttendanceBySchoolAndDateRange(@Param("schoolId") Long schoolId, @Param("start") LocalDate start, @Param("end") LocalDate end);
}
