package com.shalaconnect.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.shalaconnect.dto.request.FormRequest;
import com.shalaconnect.dto.response.ApiResponse;
import com.shalaconnect.service.FormService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/forms")
@RequiredArgsConstructor
public class FormController {

    private final FormService formService;
    private final ObjectMapper objectMapper;

    @GetMapping
    public ResponseEntity<ApiResponse<List<Map<String, Object>>>> getAllForms(
            @AuthenticationPrincipal UserDetails userDetails) {
        return ResponseEntity.ok(ApiResponse.success(
            formService.getAllForms(userDetails.getUsername())));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<Map<String, Object>>> getFormById(
            @PathVariable Long id,
            @AuthenticationPrincipal UserDetails userDetails) {
        return ResponseEntity.ok(ApiResponse.success(
            formService.getFormById(id, userDetails.getUsername())));
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<Map<String, Object>>> createForm(
            @Valid @RequestBody FormRequest request,
            @AuthenticationPrincipal UserDetails userDetails) {
        Map<String, Object> form = formService.createForm(request, userDetails.getUsername());
        return ResponseEntity.ok(ApiResponse.success("Form created successfully", form));
    }

    @PostMapping("/{id}/respond")
    @PreAuthorize("hasRole('HEADMASTER')")
    public ResponseEntity<ApiResponse<Map<String, Object>>> respondToForm(
            @PathVariable Long id,
            @RequestBody Map<String, Object> body,
            @AuthenticationPrincipal UserDetails userDetails) {
        Object answersObj = body.get("answersJson");
        if (answersObj == null) {
            answersObj = body.get("answers");
        }
        if (answersObj == null) {
            return ResponseEntity.badRequest().body(ApiResponse.error("answersJson is required"));
        }
        String answersJson;
        if (answersObj instanceof String s) {
            if (s.isBlank()) {
                return ResponseEntity.badRequest().body(ApiResponse.error("answersJson cannot be blank"));
            }
            answersJson = s;
        } else {
            try {
                answersJson = objectMapper.writeValueAsString(answersObj);
            } catch (Exception e) {
                return ResponseEntity.badRequest().body(ApiResponse.error("Invalid answers format: " + e.getMessage()));
            }
        }
        Map<String, Object> result = formService.submitFormResponse(id, answersJson, userDetails.getUsername());
        return ResponseEntity.ok(ApiResponse.success("Response submitted", result));
    }

    @GetMapping("/{id}/export")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<byte[]> exportFormResponses(@PathVariable Long id) {
        byte[] excelData = formService.exportFormResponsesAsExcel(id);
        return ResponseEntity.ok()
            .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=form-responses-" + id + ".xlsx")
            .contentType(MediaType.parseMediaType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"))
            .body(excelData);
    }

    @GetMapping("/{id}/responses")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<List<Map<String, Object>>>> getFormResponses(@PathVariable Long id) {
        return ResponseEntity.ok(ApiResponse.success(formService.getFormResponses(id)));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<Void>> deleteForm(@PathVariable Long id) {
        formService.deleteForm(id);
        return ResponseEntity.ok(ApiResponse.success("Form deleted", null));
    }
}
