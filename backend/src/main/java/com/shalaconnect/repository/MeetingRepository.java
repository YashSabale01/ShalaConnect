package com.shalaconnect.repository;

import com.shalaconnect.model.Meeting;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface MeetingRepository extends JpaRepository<Meeting, Long> {

    @Query("SELECT DISTINCT m FROM Meeting m LEFT JOIN FETCH m.createdBy LEFT JOIN FETCH m.acknowledgedBy WHERE m.active = true ORDER BY m.scheduledAt DESC")
    List<Meeting> findByActiveTrueOrderByScheduledAtDesc();

    @Query("SELECT DISTINCT m FROM Meeting m LEFT JOIN FETCH m.createdBy LEFT JOIN FETCH m.acknowledgedBy WHERE m.scheduledAt > :now AND m.active = true ORDER BY m.scheduledAt ASC")
    List<Meeting> findByScheduledAtAfterAndActiveTrue(@Param("now") LocalDateTime now);

    @Query("SELECT DISTINCT m FROM Meeting m LEFT JOIN FETCH m.createdBy LEFT JOIN FETCH m.acknowledgedBy WHERE m.status = :status AND m.active = true")
    List<Meeting> findByStatusAndActiveTrue(@Param("status") Meeting.MeetingStatus status);

    @Query("SELECT DISTINCT m FROM Meeting m LEFT JOIN FETCH m.createdBy LEFT JOIN FETCH m.acknowledgedBy WHERE m.id = :id")
    Optional<Meeting> findByIdWithDetails(@Param("id") Long id);
}
