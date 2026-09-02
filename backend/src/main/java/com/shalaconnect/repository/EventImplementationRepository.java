package com.shalaconnect.repository;

import com.shalaconnect.model.EventImplementation;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface EventImplementationRepository extends JpaRepository<EventImplementation, Long> {
    List<EventImplementation> findByEventId(Long eventId);
    Optional<EventImplementation> findByEventIdAndSchoolId(Long eventId, Long schoolId);
    List<EventImplementation> findBySubmittedById(Long userId);
}
