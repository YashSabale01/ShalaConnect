package com.shalaconnect.service;

import com.shalaconnect.dto.request.MeetingRequest;
import com.shalaconnect.dto.response.MeetingResponse;
import java.util.List;

public interface MeetingService {
    List<MeetingResponse> getAllMeetings(String currentUserEmail);
    MeetingResponse getMeetingById(Long id, String currentUserEmail);
    MeetingResponse createMeeting(MeetingRequest request, String creatorEmail);
    MeetingResponse updateMeeting(Long id, MeetingRequest request);
    MeetingResponse acknowledgeMeeting(Long id, String userEmail);
    void deleteMeeting(Long id);
    List<MeetingResponse> getUpcomingMeetings(String currentUserEmail);
}
