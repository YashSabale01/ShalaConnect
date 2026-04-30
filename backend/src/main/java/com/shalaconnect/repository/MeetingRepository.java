package com.shalaconnect.repository;

import com.shalaconnect.model.Meeting;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface MeetingRepository extends JpaRepository<Meeting, Long> {
    List<Meeting> findByActiveTrueOrderByScheduledAtDesc();
    List<Meeting> findByScheduledAtAfterAndActiveTrue(LocalDateTime now);
    List<Meeting> findByStatusAndActiveTrue(Meeting.MeetingStatus status);
}
