package com.shalaconnect.repository;

import com.shalaconnect.model.GrDocument;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface GrDocumentRepository extends JpaRepository<GrDocument, Long> {

    @Query("SELECT DISTINCT g FROM GrDocument g LEFT JOIN FETCH g.uploadedBy LEFT JOIN FETCH g.seenBy WHERE g.active = true ORDER BY g.createdAt DESC")
    List<GrDocument> findByActiveTrueOrderByCreatedAtDesc();

    @Query("SELECT DISTINCT g FROM GrDocument g LEFT JOIN FETCH g.uploadedBy LEFT JOIN FETCH g.seenBy WHERE g.grNumber LIKE %:grNumber% AND g.active = true")
    List<GrDocument> findByGrNumberContainingIgnoreCase(@Param("grNumber") String grNumber);

    @Query("SELECT DISTINCT g FROM GrDocument g LEFT JOIN FETCH g.uploadedBy LEFT JOIN FETCH g.seenBy WHERE g.id = :id")
    Optional<GrDocument> findByIdWithDetails(@Param("id") Long id);
}
