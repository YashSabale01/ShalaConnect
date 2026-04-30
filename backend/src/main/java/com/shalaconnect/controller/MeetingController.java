package com.shalaconnect.controller;

import com.shalaconnect.dto.request.MeetingRequest;
import com.shalaconnect.dto.response.ApiResponse;
import com.shalaconnect.dto.response.MeetingResponse;
import com.shalaconnect.service.MeetingService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/meetings")
@RequiredArgsConstructor
public class MeetingController {

    private final MeetingService meetingService;

    @GetMapping
    public ResponseEntity<ApiResponse<List<MeetingResponse>>> getAllMeetings(
            @AuthenticationPrincipal UserDetails userDetails) {
        return ResponseEntity.ok(ApiResponse.success(
            meetingService.getAllMeetings(userDetails.getUsername())));
    }

    @GetMapping("/upcoming")
    public ResponseEntity<ApiResponse<List<MeetingResponse>>> getUpcoming(
            @AuthenticationPrincipal UserDetails userDetails) {
        return ResponseEntity.ok(ApiResponse.success(
            meetingService.getUpcomingMeetings(userDetails.getUsername())));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<MeetingResponse>> getMeetingById(
            @PathVariable Long id,
            @AuthenticationPrincipal UserDetails userDetails) {
        return ResponseEntity.ok(ApiResponse.success(
            meetingService.getMeetingById(id, userDetails.getUsername())));
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<MeetingResponse>> createMeeting(
            @Valid @RequestBody MeetingRequest request,
            @AuthenticationPrincipal UserDetails userDetails) {
        MeetingResponse response = meetingService.createMeeting(request, userDetails.getUsername());
        return ResponseEntity.ok(ApiResponse.success("Meeting scheduled", response));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<MeetingResponse>> updateMeeting(
            @PathVariable Long id,
            @Valid @RequestBody MeetingRequest request) {
        return ResponseEntity.ok(ApiResponse.success("Meeting updated",
            meetingService.updateMeeting(id, request)));
    }

    @PostMapping("/{id}/acknowledge")
    @PreAuthorize("hasRole('HEADMASTER')")
    public ResponseEntity<ApiResponse<MeetingResponse>> acknowledge(
            @PathVariable Long id,
            @AuthenticationPrincipal UserDetails userDetails) {
        MeetingResponse response = meetingService.acknowledgeMeeting(id, userDetails.getUsername());
        return ResponseEntity.ok(ApiResponse.success("Meeting acknowledged", response));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<Void>> deleteMeeting(@PathVariable Long id) {
        meetingService.deleteMeeting(id);
        return ResponseEntity.ok(ApiResponse.success("Meeting cancelled", null));
    }
}
