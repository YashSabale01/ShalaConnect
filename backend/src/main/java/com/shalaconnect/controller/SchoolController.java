package com.shalaconnect.controller;

import com.shalaconnect.dto.request.SchoolRequest;
import com.shalaconnect.dto.response.ApiResponse;
import com.shalaconnect.dto.response.SchoolResponse;
import com.shalaconnect.service.SchoolService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@RestController
@RequestMapping("/api/schools")
@RequiredArgsConstructor
public class SchoolController {

    private final SchoolService schoolService;

    @GetMapping
    public ResponseEntity<ApiResponse<List<SchoolResponse>>> getAllSchools() {
        return ResponseEntity.ok(ApiResponse.success(schoolService.getAllSchools()));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<SchoolResponse>> getSchoolById(@PathVariable Long id) {
        return ResponseEntity.ok(ApiResponse.success(schoolService.getSchoolById(id)));
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<SchoolResponse>> createSchool(
            @Valid @RequestBody SchoolRequest.Create request) {
        return ResponseEntity.ok(ApiResponse.success("School created successfully", schoolService.createSchool(request)));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<SchoolResponse>> updateSchool(
            @PathVariable Long id,
            @Valid @RequestBody SchoolRequest.Update request) {
        return ResponseEntity.ok(ApiResponse.success("School updated successfully", schoolService.updateSchool(id, request)));
    }

    @PostMapping("/{id}/photo")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<SchoolResponse>> uploadPhoto(
            @PathVariable Long id,
            @RequestParam("file") MultipartFile file) {
        return ResponseEntity.ok(ApiResponse.success("Photo uploaded", schoolService.uploadSchoolPhoto(id, file)));
    }

    @DeleteMapping("/{id}/headmaster")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<SchoolResponse>> removeHeadmaster(@PathVariable Long id) {
        return ResponseEntity.ok(ApiResponse.success("Headmaster removed", schoolService.removeHeadmaster(id)));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<Void>> deleteSchool(@PathVariable Long id) {
        schoolService.deleteSchool(id);
        return ResponseEntity.ok(ApiResponse.success("School deleted successfully", null));
    }
}
