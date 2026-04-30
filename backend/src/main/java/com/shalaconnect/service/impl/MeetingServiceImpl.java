package com.shalaconnect.service.impl;

import com.shalaconnect.dto.request.MeetingRequest;
import com.shalaconnect.dto.response.MeetingResponse;
import com.shalaconnect.exception.ResourceNotFoundException;
import com.shalaconnect.model.Meeting;
import com.shalaconnect.model.Notification;
import com.shalaconnect.model.User;
import com.shalaconnect.repository.MeetingRepository;
import com.shalaconnect.repository.NotificationRepository;
import com.shalaconnect.repository.UserRepository;
import com.shalaconnect.service.MeetingService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class MeetingServiceImpl implements MeetingService {

    private final MeetingRepository meetingRepository;
    private final UserRepository userRepository;
    private final NotificationRepository notificationRepository;

    @Override
    @Transactional(readOnly = true)
    public List<MeetingResponse> getAllMeetings(String currentUserEmail) {
        Long userId = getUserIdByEmail(currentUserEmail);
        return meetingRepository.findByActiveTrueOrderByScheduledAtDesc().stream()
            .map(m -> MeetingResponse.from(m, userId))
            .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public MeetingResponse getMeetingById(Long id, String currentUserEmail) {
        Long userId = getUserIdByEmail(currentUserEmail);
        Meeting meeting = findById(id);
        return MeetingResponse.from(meeting, userId);
    }

    @Override
    @Transactional
    public MeetingResponse createMeeting(MeetingRequest request, String creatorEmail) {
        User creator = userRepository.findByEmail(creatorEmail)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        Meeting meeting = Meeting.builder()
            .title(request.getTitle())
            .agenda(request.getAgenda())
            .scheduledAt(request.getScheduledAt())
            .meetingType(request.getMeetingType())
            .venue(request.getVenue())
            .meetingLink(request.getMeetingLink())
            .createdBy(creator)
            .active(true)
            .build();

        meeting = meetingRepository.save(meeting);

        // Notify all headmasters
        final Long meetingId = meeting.getId();
        final String meetingTitle = meeting.getTitle();
        userRepository.findByRoleAndActiveTrue(User.Role.HEADMASTER).forEach(hm -> {
            notificationRepository.save(Notification.builder()
                .user(hm)
                .title("Meeting Scheduled")
                .message("New meeting: " + meetingTitle + " on " + request.getScheduledAt().toLocalDate())
                .type(Notification.NotificationType.MEETING)
                .referenceId(meetingId)
                .referenceType("MEETING")
                .build());
        });

        return MeetingResponse.from(meeting, creator.getId());
    }

    @Override
    @Transactional
    public MeetingResponse updateMeeting(Long id, MeetingRequest request) {
        Meeting meeting = findById(id);
        meeting.setTitle(request.getTitle());
        if (request.getAgenda() != null) meeting.setAgenda(request.getAgenda());
        meeting.setScheduledAt(request.getScheduledAt());
        meeting.setMeetingType(request.getMeetingType());
        meeting.setVenue(request.getVenue());
        meeting.setMeetingLink(request.getMeetingLink());
        return MeetingResponse.from(meetingRepository.save(meeting), null);
    }

    @Override
    @Transactional
    public MeetingResponse acknowledgeMeeting(Long id, String userEmail) {
        Meeting meeting = findById(id);
        User user = userRepository.findByEmail(userEmail)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));
        meeting.getAcknowledgedBy().add(user);
        return MeetingResponse.from(meetingRepository.save(meeting), user.getId());
    }

    @Override
    @Transactional
    public void deleteMeeting(Long id) {
        Meeting meeting = findById(id);
        meeting.setActive(false);
        meetingRepository.save(meeting);
    }

    @Override
    @Transactional(readOnly = true)
    public List<MeetingResponse> getUpcomingMeetings(String currentUserEmail) {
        Long userId = getUserIdByEmail(currentUserEmail);
        return meetingRepository.findByScheduledAtAfterAndActiveTrue(LocalDateTime.now()).stream()
            .map(m -> MeetingResponse.from(m, userId))
            .collect(Collectors.toList());
    }

    private Meeting findById(Long id) {
        return meetingRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Meeting", id));
    }

    private Long getUserIdByEmail(String email) {
        if (email == null) return null;
        return userRepository.findByEmail(email).map(User::getId).orElse(null);
    }
}
