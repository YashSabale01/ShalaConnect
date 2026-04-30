package com.shalaconnect.dto.request;

import com.shalaconnect.model.Meeting;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import java.time.LocalDateTime;

@Data
public class MeetingRequest {
    @NotBlank(message = "Title is required")
    private String title;

    private String agenda;

    @NotNull(message = "Scheduled time is required")
    private LocalDateTime scheduledAt;

    @NotNull(message = "Meeting type is required")
    private Meeting.MeetingType meetingType;

    private String venue;
    private String meetingLink;
}
