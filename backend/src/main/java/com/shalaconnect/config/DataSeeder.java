package com.shalaconnect.config;

import com.shalaconnect.model.User;
import com.shalaconnect.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
@Slf4j
public class DataSeeder implements CommandLineRunner {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) {
        if (!userRepository.existsByEmail("admin@shalaconnect.in")) {
            User admin = User.builder()
                .name("System Administrator")
                .email("admin@shalaconnect.in")
                .password(passwordEncoder.encode("Admin@123"))
                .role(User.Role.ADMIN)
                .active(true)
                .build();
            userRepository.save(admin);
            log.info("✅ Default admin created → email: admin@shalaconnect.in | password: Admin@123");
        }
    }
}
