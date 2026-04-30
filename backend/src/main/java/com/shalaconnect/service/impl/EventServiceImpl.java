package com.shalaconnect.service.impl;

import com.shalaconnect.dto.request.EventRequest;
import com.shalaconnect.dto.response.EventResponse;
import com.shalaconnect.exception.ResourceNotFoundException;
import com.shalaconnect.model.Event;
import com.shalaconnect.model.User;
import com.shalaconnect.repository.EventRepository;
import com.shalaconnect.repository.UserRepository;
import com.shalaconnect.service.EventService;
import com.shalaconnect.util.FileStorageService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class EventServiceImpl implements EventService {

    private final EventRepository eventRepository;
    private final UserRepository userRepository;
    private final FileStorageService fileStorageService;

    @Override
    @Transactional(readOnly = true)
    public List<EventResponse> getAllEvents() {
        return eventRepository.findByActiveTrueOrderByEventDateDesc().stream()
            .map(EventResponse::from).collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public EventResponse getEventById(Long id) {
        return EventResponse.from(findById(id));
    }

    @Override
    @Transactional
    public EventResponse createEvent(EventRequest request, String creatorEmail) {
        User creator = userRepository.findByEmail(creatorEmail)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        Event event = Event.builder()
            .title(request.getTitle())
            .description(request.getDescription())
            .eventDate(request.getEventDate())
            .venue(request.getVenue())
            .eventType(request.getEventType())
            .createdBy(creator)
            .active(true)
            .build();

        return EventResponse.from(eventRepository.save(event));
    }

    @Override
    @Transactional
    public EventResponse updateEvent(Long id, EventRequest request) {
        Event event = findById(id);
        event.setTitle(request.getTitle());
        if (request.getDescription() != null) event.setDescription(request.getDescription());
        event.setEventDate(request.getEventDate());
        event.setVenue(request.getVenue());
        event.setEventType(request.getEventType());
        return EventResponse.from(eventRepository.save(event));
    }

    @Override
    @Transactional
    public EventResponse uploadEventMedia(Long id, MultipartFile file) {
        fileStorageService.validateImageFile(file);
        Event event = findById(id);
        String path = fileStorageService.storeFile(file, "events/media");
        event.getMediaPaths().add(path);
        return EventResponse.from(eventRepository.save(event));
    }

    @Override
    @Transactional
    public EventResponse uploadEventReport(Long id, MultipartFile file) {
        fileStorageService.validateDocumentFile(file);
        Event event = findById(id);
        if (event.getReportPath() != null) {
            fileStorageService.deleteFile(event.getReportPath());
        }
        String path = fileStorageService.storeFile(file, "events/reports");
        event.setReportPath(path);
        event.setReportFileName(file.getOriginalFilename());
        return EventResponse.from(eventRepository.save(event));
    }

    @Override
    @Transactional
    public void deleteEvent(Long id) {
        Event event = findById(id);
        event.setActive(false);
        eventRepository.save(event);
    }

    private Event findById(Long id) {
        return eventRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Event", id));
    }
}
