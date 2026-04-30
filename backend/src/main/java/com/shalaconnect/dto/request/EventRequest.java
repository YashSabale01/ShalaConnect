package com.shalaconnect.dto.request;

import com.shalaconnect.model.Event;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import java.time.LocalDate;

@Data
public class EventRequest {
    @NotBlank(message = "Title is required")
    private String title;

    private String description;

    @NotNull(message = "Event date is required")
    private LocalDate eventDate;

    private String venue;

    @NotNull(message = "Event type is required")
    private Event.EventType eventType;
}
