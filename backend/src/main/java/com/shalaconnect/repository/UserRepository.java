package com.shalaconnect.repository;

import com.shalaconnect.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);
    List<User> findByRole(User.Role role);
    List<User> findByRoleAndActiveTrue(User.Role role);
    List<User> findBySchoolId(Long schoolId);

    @Query("SELECT u FROM User u LEFT JOIN FETCH u.school WHERE u.id = :id")
    Optional<User> findByIdWithSchool(@org.springframework.data.repository.query.Param("id") Long id);

    @Query("SELECT u FROM User u LEFT JOIN FETCH u.school")
    List<User> findAllWithSchool();

    @Query("SELECT u FROM User u LEFT JOIN FETCH u.school WHERE u.email = :email")
    Optional<User> findByEmailWithSchool(@org.springframework.data.repository.query.Param("email") String email);
}
