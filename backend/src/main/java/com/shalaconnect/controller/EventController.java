package com.shalaconnect.controller;

import com.shalaconnect.dto.request.EventRequest;
import com.shalaconnect.dto.response.ApiResponse;
import com.shalaconnect.dto.response.EventImplementationResponse;
import com.shalaconnect.dto.response.EventResponse;
import com.shalaconnect.exception.BadRequestException;
import com.shalaconnect.exception.ResourceNotFoundException;
import com.shalaconnect.model.Event;
import com.shalaconnect.model.EventImplementation;
import com.shalaconnect.model.User;
import com.shalaconnect.repository.EventImplementationRepository;
import com.shalaconnect.repository.EventRepository;
import com.shalaconnect.repository.UserRepository;
import com.shalaconnect.service.EventService;
import com.shalaconnect.util.FileStorageService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/events")
@RequiredArgsConstructor
public class EventController {

    private final EventService eventService;
    private final EventImplementationRepository implRepository;
    private final EventRepository eventRepository;
    private final UserRepository userRepository;
    private final FileStorageService fileStorageService;

    @GetMapping
    public ResponseEntity<ApiResponse<List<EventResponse>>> getAllEvents() {
        return ResponseEntity.ok(ApiResponse.success(eventService.getAllEvents()));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<EventResponse>> getEventById(@PathVariable Long id) {
        return ResponseEntity.ok(ApiResponse.success(eventService.getEventById(id)));
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<EventResponse>> createEvent(
            @Valid @RequestBody EventRequest request,
            @AuthenticationPrincipal UserDetails userDetails) {
        EventResponse response = eventService.createEvent(request, userDetails.getUsername());
        return ResponseEntity.ok(ApiResponse.success("Event created", response));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<EventResponse>> updateEvent(
            @PathVariable Long id,
            @Valid @RequestBody EventRequest request) {
        return ResponseEntity.ok(ApiResponse.success("Event updated",
            eventService.updateEvent(id, request)));
    }

    @PostMapping("/{id}/media")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<EventResponse>> uploadMedia(
            @PathVariable Long id,
            @RequestParam("file") MultipartFile file) {
        return ResponseEntity.ok(ApiResponse.success("Media uploaded",
            eventService.uploadEventMedia(id, file)));
    }

    @PostMapping("/{id}/report")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<EventResponse>> uploadReport(
            @PathVariable Long id,
            @RequestParam("file") MultipartFile file) {
        return ResponseEntity.ok(ApiResponse.success("Report uploaded",
            eventService.uploadEventReport(id, file)));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<Void>> deleteEvent(@PathVariable Long id) {
        eventService.deleteEvent(id);
        return ResponseEntity.ok(ApiResponse.success("Event deleted", null));
    }

    // ── Implementation endpoints ──────────────────────────────────────────────

    /** Headmaster submits or updates their school's implementation for an event */
    @PostMapping("/{id}/implement")
    @PreAuthorize("hasRole('HEADMASTER')")
    @org.springframework.transaction.annotation.Transactional
    public ResponseEntity<ApiResponse<EventImplementationResponse>> submitImplementation(
            @PathVariable Long id,
            @RequestBody Map<String, String> body,
            @AuthenticationPrincipal UserDetails userDetails) {
        User user = userRepository.findByEmailWithSchool(userDetails.getUsername())
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));
        if (user.getSchool() == null)
            throw new BadRequestException("You are not assigned to a school");
        Event event = eventRepository.findByIdWithCreator(id)
            .orElseThrow(() -> new ResourceNotFoundException("Event", id));

        EventImplementation impl = implRepository
            .findByEventIdAndSchoolId(id, user.getSchool().getId())
            .orElse(EventImplementation.builder().event(event).school(user.getSchool()).build());

        impl.setDescription(body.get("description"));
        impl.setSubmittedBy(user);
        implRepository.save(impl);
        // Re-fetch with JOIN FETCH to avoid lazy issues in response
        impl = implRepository.findByEventIdAndSchoolId(id, user.getSchool().getId())
            .orElseThrow(() -> new ResourceNotFoundException("Implementation not found"));
        return ResponseEntity.ok(ApiResponse.success("Implementation saved",
            EventImplementationResponse.from(impl)));
    }

    /** Headmaster uploads a photo for their implementation */
    @PostMapping("/{id}/implement/photo")
    @PreAuthorize("hasRole('HEADMASTER')")
    @org.springframework.transaction.annotation.Transactional
    public ResponseEntity<ApiResponse<EventImplementationResponse>> uploadImplPhoto(
            @PathVariable Long id,
            @RequestParam("file") MultipartFile file,
            @AuthenticationPrincipal UserDetails userDetails) {
        fileStorageService.validateImageFile(file);
        User user = userRepository.findByEmailWithSchool(userDetails.getUsername())
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));
        if (user.getSchool() == null)
            throw new BadRequestException("You are not assigned to a school");
        Event event = eventRepository.findByIdWithCreator(id)
            .orElseThrow(() -> new ResourceNotFoundException("Event", id));

        EventImplementation impl = implRepository
            .findByEventIdAndSchoolId(id, user.getSchool().getId())
            .orElse(EventImplementation.builder().event(event).school(user.getSchool()).submittedBy(user).build());

        String path = fileStorageService.storeFile(file, "events/implementations");
        impl.getPhotoPaths().add(path);
        implRepository.save(impl);
        // Re-fetch with JOIN FETCH to avoid lazy issues in response
        impl = implRepository.findByEventIdAndSchoolId(id, user.getSchool().getId())
            .orElseThrow(() -> new ResourceNotFoundException("Implementation not found"));
        return ResponseEntity.ok(ApiResponse.success("Photo uploaded",
            EventImplementationResponse.from(impl)));
    }

    /** Admin monitors all schools' implementations for an event */
    @GetMapping("/{id}/implementations")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<List<EventImplementationResponse>>> getImplementations(
            @PathVariable Long id) {
        List<EventImplementationResponse> list = implRepository.findByEventId(id)
            .stream().map(EventImplementationResponse::from).toList();
        return ResponseEntity.ok(ApiResponse.success(list));
    }

    /** Headmaster gets their own implementation for an event */
    @GetMapping("/{id}/my-implementation")
    @PreAuthorize("hasRole('HEADMASTER')")
    public ResponseEntity<ApiResponse<EventImplementationResponse>> getMyImplementation(
            @PathVariable Long id,
            @AuthenticationPrincipal UserDetails userDetails) {
        User user = userRepository.findByEmailWithSchool(userDetails.getUsername())
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));
        if (user.getSchool() == null)
            return ResponseEntity.ok(ApiResponse.success(null));
        return implRepository.findByEventIdAndSchoolId(id, user.getSchool().getId())
            .map(impl -> ResponseEntity.ok(ApiResponse.success(EventImplementationResponse.from(impl))))
            .orElse(ResponseEntity.ok(ApiResponse.success(null)));
    }
}
