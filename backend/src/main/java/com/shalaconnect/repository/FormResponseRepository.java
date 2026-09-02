package com.shalaconnect.repository;

import com.shalaconnect.model.FormResponse;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface FormResponseRepository extends JpaRepository<FormResponse, Long> {
    List<FormResponse> findByFormId(Long formId);
    Optional<FormResponse> findByFormIdAndSubmittedById(Long formId, Long userId);
    long countByFormId(Long formId);
    boolean existsByFormIdAndSubmittedById(Long formId, Long userId);
}
