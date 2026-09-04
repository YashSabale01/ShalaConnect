package com.shalaconnect.dto.response;

import com.shalaconnect.model.EventImplementation;
import lombok.*;

import java.time.LocalDateTime;
import java.util.List;

@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class EventImplementationResponse {
    private Long id;
    private Long eventId;
    private String eventTitle;
    private java.time.LocalDate eventDate;
    private Long schoolId;
    private String schoolName;
    private String submittedByName;
    private String description;
    private List<String> photoPaths;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public static EventImplementationResponse from(EventImplementation i) {
        List<String> photos;
        try { photos = i.getPhotoPaths() != null ? new java.util.ArrayList<>(new java.util.LinkedHashSet<>(i.getPhotoPaths())) : new java.util.ArrayList<>(); }
        catch (Exception e) { photos = new java.util.ArrayList<>(); }
        return EventImplementationResponse.builder()
            .id(i.getId())
            .eventId(i.getEvent() != null ? i.getEvent().getId() : null)
            .eventTitle(i.getEvent() != null ? i.getEvent().getTitle() : null)
            .eventDate(i.getEvent() != null ? i.getEvent().getEventDate() : null)
            .schoolId(i.getSchool().getId())
            .schoolName(i.getSchool().getName())
            .submittedByName(i.getSubmittedBy() != null ? i.getSubmittedBy().getName() : null)
            .description(i.getDescription())
            .photoPaths(photos)
            .createdAt(i.getCreatedAt())
            .updatedAt(i.getUpdatedAt())
            .build();
    }
}
