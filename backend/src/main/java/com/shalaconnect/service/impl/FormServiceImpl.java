package com.shalaconnect.service.impl;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.shalaconnect.dto.request.FormRequest;
import com.shalaconnect.exception.BadRequestException;
import com.shalaconnect.exception.ResourceNotFoundException;
import com.shalaconnect.model.DynamicForm;
import com.shalaconnect.model.FormResponse;
import com.shalaconnect.model.Notification;
import com.shalaconnect.model.User;
import com.shalaconnect.repository.*;
import com.shalaconnect.service.FormService;
import lombok.RequiredArgsConstructor;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.ss.util.CellRangeAddress;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class FormServiceImpl implements FormService {

    private final DynamicFormRepository formRepository;
    private final FormResponseRepository responseRepository;
    private final UserRepository userRepository;
    private final NotificationRepository notificationRepository;
    private final ObjectMapper objectMapper;

    @Override
    @Transactional(readOnly = true)
    public List<Map<String, Object>> getAllForms(String currentUserEmail) {
        User currentUser = userRepository.findByEmail(currentUserEmail).orElse(null);
        return formRepository.findByActiveTrueOrderByCreatedAtDesc().stream()
            .map(f -> toMap(f, currentUser))
            .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public Map<String, Object> getFormById(Long id, String currentUserEmail) {
        DynamicForm form = findById(id);
        User currentUser = userRepository.findByEmail(currentUserEmail).orElse(null);
        return toMap(form, currentUser);
    }

    @Override
    @Transactional
    public Map<String, Object> createForm(FormRequest request, String creatorEmail) {
        User creator = userRepository.findByEmail(creatorEmail)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        DynamicForm form = DynamicForm.builder()
            .title(request.getTitle())
            .description(request.getDescription())
            .fieldsJson(request.getFieldsJson())
            .createdBy(creator)
            .deadline(request.getDeadline())
            .active(true)
            .build();

        form = formRepository.save(form);
        final Long formId = form.getId();
        final String formTitle = form.getTitle();

        // Notify headmasters
        userRepository.findByRoleAndActiveTrue(User.Role.HEADMASTER).forEach(hm -> {
            notificationRepository.save(Notification.builder()
                .user(hm)
                .title("New Form Assigned")
                .message("Please fill out the form: " + formTitle)
                .type(Notification.NotificationType.FORM)
                .referenceId(formId)
                .referenceType("FORM")
                .build());
        });

        return toMap(form, creator);
    }

    @Override
    @Transactional
    public Map<String, Object> submitFormResponse(Long formId, String answersJson, String submitterEmail) {
        DynamicForm form = findById(formId);
        User submitter = userRepository.findByEmailWithSchool(submitterEmail)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        if (responseRepository.existsByFormIdAndSubmittedById(formId, submitter.getId())) {
            throw new BadRequestException("You have already submitted a response for this form");
        }

        FormResponse response = FormResponse.builder()
            .form(form)
            .submittedBy(submitter)
            .school(submitter.getSchool())
            .answersJson(answersJson)
            .build();

        responseRepository.save(response);

        // Notify cluster admin
        final Long formRespId = formId;
        final String schoolName = submitter.getSchool() != null ? submitter.getSchool().getName() : submitter.getName();
        final String formTitle = form.getTitle();
        userRepository.findByRoleAndActiveTrue(User.Role.ADMIN).forEach(admin -> {
            notificationRepository.save(Notification.builder()
                .user(admin)
                .title("Form Response Received")
                .message(schoolName + " submitted response for: " + formTitle)
                .type(Notification.NotificationType.FORM)
                .referenceId(formRespId)
                .referenceType("FORM")
                .build());
        });

        Map<String, Object> result = new LinkedHashMap<>();
        result.put("success", true);
        result.put("message", "Form response submitted successfully");
        return result;
    }

    @Override
    @Transactional(readOnly = true)
    public byte[] exportFormResponsesAsExcel(Long formId) {
        DynamicForm form = findById(formId);
        List<FormResponse> responses = responseRepository.findByFormId(formId);

        try (XSSFWorkbook workbook = new XSSFWorkbook()) {
            Sheet sheet = workbook.createSheet("Responses");

            // Parse fields
            List<Map<String, Object>> fields = objectMapper.readValue(
                form.getFieldsJson(), new TypeReference<>() {});

            // Header style
            CellStyle headerStyle = workbook.createCellStyle();
            Font headerFont = workbook.createFont();
            headerFont.setBold(true);
            headerStyle.setFont(headerFont);
            headerStyle.setFillForegroundColor(IndexedColors.CORNFLOWER_BLUE.getIndex());
            headerStyle.setFillPattern(FillPatternType.SOLID_FOREGROUND);

            // Header row
            Row headerRow = sheet.createRow(0);
            Cell cell0 = headerRow.createCell(0);
            cell0.setCellValue("School");
            cell0.setCellStyle(headerStyle);
            Cell cell1 = headerRow.createCell(1);
            cell1.setCellValue("Submitted By");
            cell1.setCellStyle(headerStyle);
            Cell cell2 = headerRow.createCell(2);
            cell2.setCellValue("Submitted At");
            cell2.setCellStyle(headerStyle);
            Cell cell3 = headerRow.createCell(3);
            cell3.setCellValue("Row #");
            cell3.setCellStyle(headerStyle);

            for (int i = 0; i < fields.size(); i++) {
                Cell c = headerRow.createCell(4 + i);
                c.setCellValue((String) fields.get(i).getOrDefault("label", "Field " + i));
                c.setCellStyle(headerStyle);
            }

            // Metadata cell style (vertically centered for multi-row schools)
            CellStyle metaStyle = workbook.createCellStyle();
            metaStyle.setVerticalAlignment(VerticalAlignment.CENTER);

            // Data rows
            DateTimeFormatter dtf = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm");
            int currentRowIdx = 1;
            for (FormResponse resp : responses) {
                String schoolName = resp.getSchool() != null ? resp.getSchool().getName() : "";
                String submitterName = resp.getSubmittedBy() != null ? resp.getSubmittedBy().getName() : "";
                String submittedAt = resp.getSubmittedAt() != null ? resp.getSubmittedAt().format(dtf) : "";

                List<Map<String, Object>> rowEntries = new ArrayList<>();
                try {
                    JsonNode rootNode = objectMapper.readTree(resp.getAnswersJson());
                    if (rootNode.isArray()) {
                        for (JsonNode item : rootNode) {
                            rowEntries.add(objectMapper.convertValue(item, new TypeReference<Map<String, Object>>() {}));
                        }
                    } else if (rootNode.has("rows") && rootNode.get("rows").isArray()) {
                        for (JsonNode item : rootNode.get("rows")) {
                            rowEntries.add(objectMapper.convertValue(item, new TypeReference<Map<String, Object>>() {}));
                        }
                    } else {
                        rowEntries.add(objectMapper.convertValue(rootNode, new TypeReference<Map<String, Object>>() {}));
                    }
                } catch (Exception e) {
                    rowEntries.add(Collections.emptyMap());
                }

                if (rowEntries.isEmpty()) {
                    rowEntries.add(Collections.emptyMap());
                }

                int startRowIdx = currentRowIdx;
                int entryNum = 1;
                for (Map<String, Object> entryMap : rowEntries) {
                    Row row = sheet.createRow(currentRowIdx++);

                    // Set School metadata only on the first row of this school's entry
                    Cell c0 = row.createCell(0);
                    Cell c1 = row.createCell(1);
                    Cell c2 = row.createCell(2);
                    c0.setCellStyle(metaStyle);
                    c1.setCellStyle(metaStyle);
                    c2.setCellStyle(metaStyle);

                    if (entryNum == 1) {
                        c0.setCellValue(schoolName);
                        c1.setCellValue(submitterName);
                        c2.setCellValue(submittedAt);
                    }

                    row.createCell(3).setCellValue(entryNum++);

                    for (int f = 0; f < fields.size(); f++) {
                        String fieldId = (String) fields.get(f).getOrDefault("id", "");
                        Object answer = entryMap.getOrDefault(fieldId, "");
                        row.createCell(4 + f).setCellValue(answer != null ? answer.toString() : "");
                    }
                }

                // If school submitted multiple rows, merge school metadata vertically across the rows
                if (rowEntries.size() > 1) {
                    int endRowIdx = currentRowIdx - 1;
                    sheet.addMergedRegion(new CellRangeAddress(startRowIdx, endRowIdx, 0, 0));
                    sheet.addMergedRegion(new CellRangeAddress(startRowIdx, endRowIdx, 1, 1));
                    sheet.addMergedRegion(new CellRangeAddress(startRowIdx, endRowIdx, 2, 2));
                }
            }

            for (int i = 0; i < fields.size() + 4; i++) sheet.autoSizeColumn(i);

            ByteArrayOutputStream bos = new ByteArrayOutputStream();
            workbook.write(bos);
            return bos.toByteArray();
        } catch (IOException e) {
            throw new RuntimeException("Failed to export Excel: " + e.getMessage());
        }
    }

    @Override
    @Transactional
    public void deleteForm(Long id) {
        DynamicForm form = findById(id);
        form.setActive(false);
        formRepository.save(form);
    }

    private DynamicForm findById(Long id) {
        return formRepository.findByIdWithCreator(id)
            .orElseThrow(() -> new ResourceNotFoundException("Form", id));
    }

    private Map<String, Object> toMap(DynamicForm form, User currentUser) {
        Map<String, Object> map = new LinkedHashMap<>();
        map.put("id", form.getId());
        map.put("title", form.getTitle());
        map.put("description", form.getDescription());
        map.put("fieldsJson", form.getFieldsJson());
        map.put("deadline", form.getDeadline());
        map.put("createdAt", form.getCreatedAt());
        map.put("createdByName", form.getCreatedBy() != null ? form.getCreatedBy().getName() : null);
        map.put("responseCount", responseRepository.countByFormId(form.getId()));
        if (currentUser != null) {
            boolean hasResponded = responseRepository
                .existsByFormIdAndSubmittedById(form.getId(), currentUser.getId());
            map.put("hasResponded", hasResponded);
        } else {
            map.put("hasResponded", false);
        }
        return map;
    }
}
