package com.shalaconnect.service;

import com.shalaconnect.dto.request.EventRequest;
import com.shalaconnect.dto.response.EventResponse;
import org.springframework.web.multipart.MultipartFile;
import java.util.List;

public interface EventService {
    List<EventResponse> getAllEvents();
    EventResponse getEventById(Long id);
    EventResponse createEvent(EventRequest request, String creatorEmail);
    EventResponse updateEvent(Long id, EventRequest request);
    EventResponse uploadEventMedia(Long id, MultipartFile file);
    EventResponse uploadEventReport(Long id, MultipartFile file);
    void deleteEvent(Long id);
}
