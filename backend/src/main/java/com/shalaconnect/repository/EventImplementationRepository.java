package com.shalaconnect.repository;

import com.shalaconnect.model.EventImplementation;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface EventImplementationRepository extends JpaRepository<EventImplementation, Long> {

    @Query("SELECT i FROM EventImplementation i LEFT JOIN FETCH i.event LEFT JOIN FETCH i.school LEFT JOIN FETCH i.submittedBy WHERE i.event.id = :eventId")
    List<EventImplementation> findByEventId(@Param("eventId") Long eventId);

    @Query("SELECT i FROM EventImplementation i LEFT JOIN FETCH i.event LEFT JOIN FETCH i.school LEFT JOIN FETCH i.submittedBy WHERE i.event.id = :eventId AND i.school.id = :schoolId")
    Optional<EventImplementation> findByEventIdAndSchoolId(@Param("eventId") Long eventId, @Param("schoolId") Long schoolId);

    List<EventImplementation> findBySubmittedById(Long userId);
}
