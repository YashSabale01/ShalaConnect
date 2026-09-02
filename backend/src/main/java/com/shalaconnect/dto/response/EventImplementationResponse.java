package com.shalaconnect.dto.response;

import com.shalaconnect.model.EventImplementation;
import lombok.*;

import java.time.LocalDateTime;
import java.util.List;

@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class EventImplementationResponse {
    private Long id;
    private Long eventId;
    private Long schoolId;
    private String schoolName;
    private String submittedByName;
    private String description;
    private List<String> photoPaths;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public static EventImplementationResponse from(EventImplementation i) {
        return EventImplementationResponse.builder()
            .id(i.getId())
            .eventId(i.getEvent().getId())
            .schoolId(i.getSchool().getId())
            .schoolName(i.getSchool().getName())
            .submittedByName(i.getSubmittedBy() != null ? i.getSubmittedBy().getName() : null)
            .description(i.getDescription())
            .photoPaths(i.getPhotoPaths())
            .createdAt(i.getCreatedAt())
            .updatedAt(i.getUpdatedAt())
            .build();
    }
}
