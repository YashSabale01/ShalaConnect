package com.shalaconnect.dto.response;

import com.shalaconnect.model.*;
import lombok.*;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class GrDocumentResponse {
    private Long id;
    private String title;
    private String description;
    private String grNumber;
    private String filePath;
    private String fileName;
    private Long fileSize;
    private String uploadedByName;
    private int seenCount;
    private boolean seenByCurrentUser;
    private LocalDateTime expiresAt;
    private LocalDateTime createdAt;

    public static GrDocumentResponse from(GrDocument d, Long currentUserId) {
        return GrDocumentResponse.builder()
            .id(d.getId()).title(d.getTitle()).description(d.getDescription())
            .grNumber(d.getGrNumber()).filePath(d.getFilePath()).fileName(d.getFileName())
            .fileSize(d.getFileSize())
            .uploadedByName(d.getUploadedBy() != null ? d.getUploadedBy().getName() : null)
            .seenCount(d.getSeenBy().size())
            .seenByCurrentUser(currentUserId != null && d.getSeenBy().stream().anyMatch(u -> u.getId().equals(currentUserId)))
            .expiresAt(d.getExpiresAt()).createdAt(d.getCreatedAt()).build();
    }
}
