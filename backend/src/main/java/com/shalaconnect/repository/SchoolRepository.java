package com.shalaconnect.repository;

import com.shalaconnect.model.School;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface SchoolRepository extends JpaRepository<School, Long> {
    List<School> findByActiveTrue();
    Optional<School> findByUdiseCode(String udiseCode);
    boolean existsByUdiseCode(String udiseCode);

    @Query("SELECT s FROM School s WHERE s.active = true ORDER BY s.name ASC")
    List<School> findAllActiveSortedByName();
}
