package com.shalaconnect.dto.response;

import com.shalaconnect.model.Notification;
import lombok.*;
import java.time.LocalDateTime;

@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class NotificationResponse {
    private Long id;
    private String title;
    private String message;
    private String type;
    private Long referenceId;
    private String referenceType;
    private boolean read;
    private LocalDateTime createdAt;

    public static NotificationResponse from(Notification n) {
        return NotificationResponse.builder()
            .id(n.getId()).title(n.getTitle()).message(n.getMessage())
            .type(n.getType() != null ? n.getType().name() : null)
            .referenceId(n.getReferenceId()).referenceType(n.getReferenceType())
            .read(n.isRead()).createdAt(n.getCreatedAt()).build();
    }
}
