package com.shalaconnect.repository;

import com.shalaconnect.model.DynamicForm;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface DynamicFormRepository extends JpaRepository<DynamicForm, Long> {

    @Query("SELECT f FROM DynamicForm f LEFT JOIN FETCH f.createdBy WHERE f.active = true ORDER BY f.createdAt DESC")
    List<DynamicForm> findByActiveTrueOrderByCreatedAtDesc();

    @Query("SELECT f FROM DynamicForm f LEFT JOIN FETCH f.createdBy WHERE f.id = :id")
    Optional<DynamicForm> findByIdWithCreator(@Param("id") Long id);
}
