package com.shalaconnect.repository;

import com.shalaconnect.model.FormResponse;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface FormResponseRepository extends JpaRepository<FormResponse, Long> {

    @Query("SELECT r FROM FormResponse r LEFT JOIN FETCH r.submittedBy LEFT JOIN FETCH r.school WHERE r.form.id = :formId")
    List<FormResponse> findByFormId(@Param("formId") Long formId);

    Optional<FormResponse> findByFormIdAndSubmittedById(Long formId, Long userId);
    long countByFormId(Long formId);
    boolean existsByFormIdAndSubmittedById(Long formId, Long userId);
}
