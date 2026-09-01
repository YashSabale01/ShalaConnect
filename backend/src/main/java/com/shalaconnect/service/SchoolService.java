package com.shalaconnect.service;

import com.shalaconnect.dto.request.SchoolRequest;
import com.shalaconnect.dto.response.SchoolResponse;
import org.springframework.web.multipart.MultipartFile;
import java.util.List;

public interface SchoolService {
    List<SchoolResponse> getAllSchools();
    SchoolResponse getSchoolById(Long id);
    SchoolResponse createSchool(SchoolRequest.Create request);
    SchoolResponse updateSchool(Long id, SchoolRequest.Update request);
    SchoolResponse uploadSchoolPhoto(Long id, MultipartFile file);
    void deleteSchool(Long id);
    List<SchoolResponse> getActiveSchools();
    SchoolResponse removeHeadmaster(Long schoolId);
}
