package com.shalaconnect.config;

import com.shalaconnect.model.User;
import com.shalaconnect.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.env.Environment;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
@Slf4j
public class DataSeeder implements CommandLineRunner {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final Environment env;
    private final JdbcTemplate jdbcTemplate;

    @Override
    public void run(String... args) {
        // Ensure answers_json in form_responses is TEXT in PostgreSQL
        try {
            jdbcTemplate.execute("ALTER TABLE form_responses ALTER COLUMN answers_json TYPE TEXT;");
            log.info("✅ Verified form_responses.answers_json column is TYPE TEXT");
        } catch (Exception e) {
            log.debug("form_responses table/column migration note: {}", e.getMessage());
        }

        String adminEmail    = System.getenv("ADMIN_EMAIL")    != null ? System.getenv("ADMIN_EMAIL")    : env.getProperty("app.admin.email");
        String adminPassword = System.getenv("ADMIN_PASSWORD") != null ? System.getenv("ADMIN_PASSWORD") : env.getProperty("app.admin.password");

        if (adminEmail == null || adminEmail.isBlank() || adminPassword == null || adminPassword.isBlank()) {
            log.warn("⚠️  ADMIN_EMAIL or ADMIN_PASSWORD not set — skipping admin seed");
            return;
        }

        if (!userRepository.existsByEmail(adminEmail)) {
            User admin = User.builder()
                .name("System Administrator")
                .email(adminEmail)
                .password(passwordEncoder.encode(adminPassword))
                .role(User.Role.ADMIN)
                .active(true)
                .build();
            userRepository.save(admin);
            log.info("✅ Default admin created");
        }
    }
}
