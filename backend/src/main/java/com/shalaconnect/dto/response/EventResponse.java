package com.shalaconnect.dto.response;

import com.shalaconnect.model.Event;
import lombok.*;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class EventResponse {
    private Long id;
    private String title;
    private String description;
    private LocalDate eventDate;
    private String venue;
    private String eventType;
    private String createdByName;
    private List<String> mediaPaths;
    private String reportPath;
    private LocalDateTime createdAt;

    public static EventResponse from(Event e) {
        return EventResponse.builder()
            .id(e.getId()).title(e.getTitle()).description(e.getDescription())
            .eventDate(e.getEventDate()).venue(e.getVenue())
            .eventType(e.getEventType().name())
            .createdByName(e.getCreatedBy() != null ? e.getCreatedBy().getName() : null)
            .mediaPaths(e.getMediaPaths()).reportPath(e.getReportPath())
            .createdAt(e.getCreatedAt()).build();
    }
}
