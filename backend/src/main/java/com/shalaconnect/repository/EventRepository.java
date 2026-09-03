package com.shalaconnect.repository;

import com.shalaconnect.model.Event;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Repository
public interface EventRepository extends JpaRepository<Event, Long> {

    @Query("SELECT e FROM Event e LEFT JOIN FETCH e.createdBy WHERE e.active = true ORDER BY e.eventDate DESC")
    List<Event> findByActiveTrueOrderByEventDateDesc();

    @Query("SELECT e FROM Event e LEFT JOIN FETCH e.createdBy WHERE e.id = :id")
    Optional<Event> findByIdWithCreator(@Param("id") Long id);

    List<Event> findByEventDateBetweenAndActiveTrue(LocalDate start, LocalDate end);
    List<Event> findByEventTypeAndActiveTrue(Event.EventType eventType);
}
