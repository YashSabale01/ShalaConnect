package com.shalaconnect.repository;

import com.shalaconnect.model.GrDocument;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface GrDocumentRepository extends JpaRepository<GrDocument, Long> {
    List<GrDocument> findByActiveTrueOrderByCreatedAtDesc();
    List<GrDocument> findByGrNumberContainingIgnoreCase(String grNumber);
}
