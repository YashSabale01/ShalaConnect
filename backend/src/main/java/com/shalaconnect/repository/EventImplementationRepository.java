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

    // For list view — fetch associations but NOT the ElementCollection (avoids MultipleBagFetchException)
    @Query("SELECT i FROM EventImplementation i LEFT JOIN FETCH i.school LEFT JOIN FETCH i.submittedBy WHERE i.event.id = :eventId")
    List<EventImplementation> findByEventId(@Param("eventId") Long eventId);

    // For single entity — fetch associations only
    @Query("SELECT i FROM EventImplementation i LEFT JOIN FETCH i.school LEFT JOIN FETCH i.submittedBy WHERE i.event.id = :eventId AND i.school.id = :schoolId")
    Optional<EventImplementation> findByEventIdAndSchoolId(@Param("eventId") Long eventId, @Param("schoolId") Long schoolId);

    // Fetch photoPaths ElementCollection separately (called after findByEventIdAndSchoolId)
    @Query("SELECT i FROM EventImplementation i LEFT JOIN FETCH i.photoPaths WHERE i.id = :id")
    Optional<EventImplementation> findByIdWithPhotos(@Param("id") Long id);

    List<EventImplementation> findBySubmittedById(Long userId);
}
