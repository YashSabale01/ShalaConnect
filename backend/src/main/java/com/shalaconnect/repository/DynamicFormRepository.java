package com.shalaconnect.repository;

import com.shalaconnect.model.DynamicForm;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface DynamicFormRepository extends JpaRepository<DynamicForm, Long> {
    List<DynamicForm> findByActiveTrueOrderByCreatedAtDesc();
}
