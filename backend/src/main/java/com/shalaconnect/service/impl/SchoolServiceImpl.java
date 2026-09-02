package com.shalaconnect.service.impl;

import com.shalaconnect.dto.request.SchoolRequest;
import com.shalaconnect.dto.response.SchoolResponse;
import com.shalaconnect.exception.BadRequestException;
import com.shalaconnect.exception.ResourceNotFoundException;
import com.shalaconnect.model.School;
import com.shalaconnect.repository.SchoolRepository;
import com.shalaconnect.repository.UserRepository;
import com.shalaconnect.service.SchoolService;
import com.shalaconnect.util.FileStorageService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class SchoolServiceImpl implements SchoolService {

    private final SchoolRepository schoolRepository;
    private final UserRepository userRepository;
    private final FileStorageService fileStorageService;

    @Override
    @Transactional(readOnly = true)
    public List<SchoolResponse> getAllSchools() {
        return schoolRepository.findAllActiveSortedByNameWithStaff().stream()
            .map(SchoolResponse::from)
            .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public SchoolResponse getSchoolById(Long id) {
        return SchoolResponse.from(schoolRepository.findByIdWithStaff(id)
            .orElseThrow(() -> new ResourceNotFoundException("School", id)));
    }

    @Override
    @Transactional
    public SchoolResponse createSchool(SchoolRequest.Create request) {
        if (schoolRepository.existsByUdiseCode(request.getUdiseCode())) {
            throw new BadRequestException("A school with UDISE code '" + request.getUdiseCode() + "' already exists");
        }

        School school = School.builder()
            .name(request.getName())
            .udiseCode(request.getUdiseCode())
            .address(request.getAddress())
            .village(request.getVillage())
            .taluka(request.getTaluka())
            .district(request.getDistrict())
            .pincode(request.getPincode())
            .phone(request.getPhone())
            .email(request.getEmail())
            .totalStudents(request.getTotalStudents())
            .totalTeachers(request.getTotalTeachers())
            .topperName(request.getTopperName())
            .topperPercentage(request.getTopperPercentage())
            .topperClass(request.getTopperClass())
            .active(true)
            .build();

        return SchoolResponse.from(schoolRepository.save(school));
    }

    @Override
    @Transactional
    public SchoolResponse updateSchool(Long id, SchoolRequest.Update request) {
        School school = findSchoolById(id);

        if (request.getName() != null) school.setName(request.getName());
        if (request.getAddress() != null) school.setAddress(request.getAddress());
        if (request.getVillage() != null) school.setVillage(request.getVillage());
        if (request.getTaluka() != null) school.setTaluka(request.getTaluka());
        if (request.getDistrict() != null) school.setDistrict(request.getDistrict());
        if (request.getPincode() != null) school.setPincode(request.getPincode());
        if (request.getPhone() != null) school.setPhone(request.getPhone());
        if (request.getEmail() != null) school.setEmail(request.getEmail());
        if (request.getTotalStudents() != null) school.setTotalStudents(request.getTotalStudents());
        if (request.getTotalTeachers() != null) school.setTotalTeachers(request.getTotalTeachers());
        if (request.getTopperName() != null) school.setTopperName(request.getTopperName());
        if (request.getTopperPercentage() != null) school.setTopperPercentage(request.getTopperPercentage());
        if (request.getTopperClass() != null) school.setTopperClass(request.getTopperClass());

        return SchoolResponse.from(schoolRepository.save(school));
    }

    @Override
    @Transactional
    public SchoolResponse uploadSchoolPhoto(Long id, MultipartFile file) {
        fileStorageService.validateImageFile(file);
        School school = findSchoolById(id);
        if (school.getSchoolPhoto() != null) {
            fileStorageService.deleteFile(school.getSchoolPhoto());
        }
        String path = fileStorageService.storeFile(file, "schools");
        school.setSchoolPhoto(path);
        return SchoolResponse.from(schoolRepository.save(school));
    }

    @Override
    @Transactional
    public void deleteSchool(Long id) {
        School school = findSchoolById(id);
        school.setActive(false);
        schoolRepository.save(school);
    }

    @Override
    @Transactional(readOnly = true)
    public List<SchoolResponse> getActiveSchools() {
        return schoolRepository.findByActiveTrue().stream()
            .map(SchoolResponse::from)
            .collect(Collectors.toList());
    }

    @Override
    @Transactional
    public SchoolResponse removeHeadmaster(Long schoolId) {
        findSchoolById(schoolId);
        userRepository.findBySchoolId(schoolId).stream()
            .filter(u -> u.getRole() == com.shalaconnect.model.User.Role.HEADMASTER)
            .forEach(u -> { u.setSchool(null); userRepository.save(u); });
        return SchoolResponse.from(schoolRepository.findByIdWithStaff(schoolId)
            .orElseThrow(() -> new ResourceNotFoundException("School", schoolId)));
    }

    private School findSchoolById(Long id) {
        return schoolRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("School", id));
    }
}
