package com.shalaconnect.service;

import com.shalaconnect.dto.response.GrDocumentResponse;
import org.springframework.web.multipart.MultipartFile;
import java.util.List;

public interface GrDocumentService {
    List<GrDocumentResponse> getAllGrDocuments(String currentUserEmail);
    GrDocumentResponse getGrDocumentById(Long id, String currentUserEmail);
    GrDocumentResponse uploadGrDocument(String title, String description, String grNumber,
                                        MultipartFile file, String uploaderEmail);
    GrDocumentResponse markAsSeen(Long id, String userEmail);
    void deleteGrDocument(Long id);
}
