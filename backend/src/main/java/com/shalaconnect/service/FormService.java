package com.shalaconnect.service;

import com.shalaconnect.dto.request.FormRequest;
import com.shalaconnect.dto.response.ApiResponse;
import com.shalaconnect.model.DynamicForm;
import org.springframework.http.ResponseEntity;
import java.util.List;
import java.util.Map;

public interface FormService {
    List<Map<String, Object>> getAllForms(String currentUserEmail);
    Map<String, Object> getFormById(Long id, String currentUserEmail);
    Map<String, Object> createForm(FormRequest request, String creatorEmail);
    Map<String, Object> submitFormResponse(Long formId, String answersJson, String submitterEmail);
    byte[] exportFormResponsesAsExcel(Long formId);
    List<Map<String, Object>> getFormResponses(Long formId);
    void deleteForm(Long id);
}
