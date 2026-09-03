package com.shalaconnect.service.impl;

import com.shalaconnect.dto.response.GrDocumentResponse;
import com.shalaconnect.exception.ResourceNotFoundException;
import com.shalaconnect.model.GrDocument;
import com.shalaconnect.model.Notification;
import com.shalaconnect.model.User;
import com.shalaconnect.repository.*;
import com.shalaconnect.service.GrDocumentService;
import com.shalaconnect.util.FileStorageService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class GrDocumentServiceImpl implements GrDocumentService {

    private final GrDocumentRepository grDocumentRepository;
    private final UserRepository userRepository;
    private final NotificationRepository notificationRepository;
    private final FileStorageService fileStorageService;

    @Override
    @Transactional(readOnly = true)
    public List<GrDocumentResponse> getAllGrDocuments(String currentUserEmail) {
        Long userId = getUserIdByEmail(currentUserEmail);
        return grDocumentRepository.findByActiveTrueOrderByCreatedAtDesc().stream()
            .map(d -> GrDocumentResponse.from(d, userId))
            .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public GrDocumentResponse getGrDocumentById(Long id, String currentUserEmail) {
        Long userId = getUserIdByEmail(currentUserEmail);
        GrDocument doc = grDocumentRepository.findByIdWithDetails(id)
            .orElseThrow(() -> new ResourceNotFoundException("GR Document", id));
        return GrDocumentResponse.from(doc, userId);
    }

    @Override
    @Transactional
    public GrDocumentResponse uploadGrDocument(String title, String description, String grNumber,
                                               MultipartFile file, String uploaderEmail) {
        fileStorageService.validateDocumentFile(file);
        User uploader = userRepository.findByEmail(uploaderEmail)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        String filePath = fileStorageService.storeFile(file, "gr-documents");

        GrDocument doc = GrDocument.builder()
            .title(title)
            .description(description)
            .grNumber(grNumber)
            .filePath(filePath)
            .fileName(file.getOriginalFilename())
            .fileSize(file.getSize())
            .uploadedBy(uploader)
            .active(true)
            .build();

        doc = grDocumentRepository.save(doc);

        // Notify all headmasters
        final Long docId = doc.getId();
        final String docTitle = doc.getTitle();
        userRepository.findByRoleAndActiveTrue(User.Role.HEADMASTER).forEach(hm -> {
            Notification notification = Notification.builder()
                .user(hm)
                .title("New GR Document")
                .message("A new GR has been uploaded: " + docTitle)
                .type(Notification.NotificationType.GR_DOCUMENT)
                .referenceId(docId)
                .referenceType("GR")
                .build();
            notificationRepository.save(notification);
        });

        return GrDocumentResponse.from(doc, uploader.getId());
    }

    @Override
    @Transactional
    public GrDocumentResponse markAsSeen(Long id, String userEmail) {
        GrDocument doc = grDocumentRepository.findByIdWithDetails(id)
            .orElseThrow(() -> new ResourceNotFoundException("GR Document", id));
        User user = userRepository.findByEmail(userEmail)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));
        doc.getSeenBy().add(user);
        grDocumentRepository.save(doc);
        return GrDocumentResponse.from(doc, user.getId());
    }

    @Override
    @Transactional
    public void deleteGrDocument(Long id) {
        GrDocument doc = grDocumentRepository.findByIdWithDetails(id)
            .orElseThrow(() -> new ResourceNotFoundException("GR Document", id));
        doc.setActive(false);
        grDocumentRepository.save(doc);
    }

    private Long getUserIdByEmail(String email) {
        if (email == null) return null;
        return userRepository.findByEmail(email).map(User::getId).orElse(null);
    }
}
