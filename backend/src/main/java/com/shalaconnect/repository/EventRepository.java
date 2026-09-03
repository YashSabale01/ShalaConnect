package com.shalaconnect.repository;

import com.shalaconnect.model.Event;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.time.LocalDate;
import java.util.List;

@Repository
public interface EventRepository extends JpaRepository<Event, Long> {

    @Query("SELECT e FROM Event e LEFT JOIN FETCH e.createdBy WHERE e.active = true ORDER BY e.eventDate DESC")
    List<Event> findByActiveTrueOrderByEventDateDesc();

    List<Event> findByEventDateBetweenAndActiveTrue(LocalDate start, LocalDate end);
    List<Event> findByEventTypeAndActiveTrue(Event.EventType eventType);
}
