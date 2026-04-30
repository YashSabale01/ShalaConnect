package com.shalaconnect.controller;

import com.shalaconnect.dto.response.ApiResponse;
import com.shalaconnect.dto.response.GrDocumentResponse;
import com.shalaconnect.service.GrDocumentService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@RestController
@RequestMapping("/api/gr")
@RequiredArgsConstructor
public class GrDocumentController {

    private final GrDocumentService grDocumentService;

    @GetMapping
    public ResponseEntity<ApiResponse<List<GrDocumentResponse>>> getAllGrDocuments(
            @AuthenticationPrincipal UserDetails userDetails) {
        String email = userDetails != null ? userDetails.getUsername() : null;
        return ResponseEntity.ok(ApiResponse.success(grDocumentService.getAllGrDocuments(email)));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<GrDocumentResponse>> getGrDocument(
            @PathVariable Long id,
            @AuthenticationPrincipal UserDetails userDetails) {
        String email = userDetails != null ? userDetails.getUsername() : null;
        return ResponseEntity.ok(ApiResponse.success(grDocumentService.getGrDocumentById(id, email)));
    }

    @PostMapping(consumes = "multipart/form-data")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<GrDocumentResponse>> uploadGrDocument(
            @RequestParam("title") String title,
            @RequestParam(value = "description", required = false) String description,
            @RequestParam("grNumber") String grNumber,
            @RequestParam("file") MultipartFile file,
            @AuthenticationPrincipal UserDetails userDetails) {
        GrDocumentResponse response = grDocumentService.uploadGrDocument(
            title, description, grNumber, file, userDetails.getUsername());
        return ResponseEntity.ok(ApiResponse.success("GR document uploaded successfully", response));
    }

    @PostMapping("/{id}/seen")
    public ResponseEntity<ApiResponse<GrDocumentResponse>> markAsSeen(
            @PathVariable Long id,
            @AuthenticationPrincipal UserDetails userDetails) {
        GrDocumentResponse response = grDocumentService.markAsSeen(id, userDetails.getUsername());
        return ResponseEntity.ok(ApiResponse.success("Marked as seen", response));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<Void>> deleteGrDocument(@PathVariable Long id) {
        grDocumentService.deleteGrDocument(id);
        return ResponseEntity.ok(ApiResponse.success("GR document deleted", null));
    }
}
