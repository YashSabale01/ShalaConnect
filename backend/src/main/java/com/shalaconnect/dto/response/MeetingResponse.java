package com.shalaconnect.dto.response;

import com.shalaconnect.model.Meeting;
import lombok.*;
import java.time.LocalDateTime;

@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class MeetingResponse {
    private Long id;
    private String title;
    private String agenda;
    private LocalDateTime scheduledAt;
    private String meetingType;
    private String venue;
    private String meetingLink;
    private String status;
    private String createdByName;
    private int acknowledgedCount;
    private boolean acknowledgedByCurrentUser;
    private LocalDateTime createdAt;

    public static MeetingResponse from(Meeting m, Long currentUserId) {
        return MeetingResponse.builder()
            .id(m.getId()).title(m.getTitle()).agenda(m.getAgenda())
            .scheduledAt(m.getScheduledAt()).meetingType(m.getMeetingType().name())
            .venue(m.getVenue()).meetingLink(m.getMeetingLink())
            .status(m.getStatus() != null ? m.getStatus().name() : null)
            .createdByName(m.getCreatedBy() != null ? m.getCreatedBy().getName() : null)
            .acknowledgedCount(m.getAcknowledgedBy().size())
            .acknowledgedByCurrentUser(currentUserId != null && m.getAcknowledgedBy().stream().anyMatch(u -> u.getId().equals(currentUserId)))
            .createdAt(m.getCreatedAt()).build();
    }
}
