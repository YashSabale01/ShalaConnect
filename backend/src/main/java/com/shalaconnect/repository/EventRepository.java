package com.shalaconnect.repository;

import com.shalaconnect.model.Event;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.time.LocalDate;
import java.util.List;

@Repository
public interface EventRepository extends JpaRepository<Event, Long> {
    List<Event> findByActiveTrueOrderByEventDateDesc();
    List<Event> findByEventDateBetweenAndActiveTrue(LocalDate start, LocalDate end);
    List<Event> findByEventTypeAndActiveTrue(Event.EventType eventType);
}
