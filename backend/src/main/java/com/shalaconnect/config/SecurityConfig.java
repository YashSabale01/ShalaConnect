package com.shalaconnect.config;

import com.shalaconnect.security.JwtAuthFilter;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.Arrays;
import java.util.List;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    private final JwtAuthFilter jwtAuthFilter;
    private final UserDetailsService userDetailsService;

    @Value("${app.cors.allowed-origins}")
    private String allowedOrigins;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .csrf(AbstractHttpConfigurer::disable)
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                // Public endpoints
                .requestMatchers("/api/auth/login").permitAll()
                .requestMatchers(HttpMethod.GET, "/api/schools").permitAll()
                .requestMatchers(HttpMethod.GET, "/api/schools/**").permitAll()
                .requestMatchers(HttpMethod.GET, "/api/attendance/school/**").permitAll()
                .requestMatchers(HttpMethod.GET, "/api/events").permitAll()
                .requestMatchers("/api/health").permitAll()
                .requestMatchers("/uploads/**").permitAll()
                // Headmaster-specific POST endpoints — must come BEFORE broad admin POST rules
                .requestMatchers(HttpMethod.POST, "/api/attendance").hasRole("HEADMASTER")
                .requestMatchers(HttpMethod.POST, "/api/forms/*/respond").hasRole("HEADMASTER")
                .requestMatchers(HttpMethod.POST, "/api/meetings/*/acknowledge").hasRole("HEADMASTER")
                .requestMatchers(HttpMethod.POST, "/api/events/*/implement").hasRole("HEADMASTER")
                .requestMatchers(HttpMethod.POST, "/api/events/*/implement/photo").hasRole("HEADMASTER")
                .requestMatchers(HttpMethod.POST, "/api/gr/*/seen").authenticated()
                // Admin-only
                .requestMatchers("/api/auth/register-headmaster").hasRole("ADMIN")
                .requestMatchers(HttpMethod.POST, "/api/schools").hasRole("ADMIN")
                .requestMatchers(HttpMethod.POST, "/api/schools/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.PUT, "/api/schools/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.DELETE, "/api/schools/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.POST, "/api/gr").hasRole("ADMIN")
                .requestMatchers(HttpMethod.DELETE, "/api/gr/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.POST, "/api/meetings").hasRole("ADMIN")
                .requestMatchers(HttpMethod.PUT, "/api/meetings/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.DELETE, "/api/meetings/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.POST, "/api/events").hasRole("ADMIN")
                .requestMatchers(HttpMethod.PUT, "/api/events/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.DELETE, "/api/events/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.POST, "/api/forms").hasRole("ADMIN")
                .requestMatchers(HttpMethod.GET, "/api/forms/*/export").hasRole("ADMIN")
                .requestMatchers(HttpMethod.DELETE, "/api/forms/**").hasRole("ADMIN")
                .requestMatchers("/api/users/**").hasRole("ADMIN")
                // PUT for attendance
                .requestMatchers(HttpMethod.PUT, "/api/attendance/**").hasAnyRole("ADMIN", "HEADMASTER")
                // All other requests require authentication
                .anyRequest().authenticated()
            )
            .authenticationProvider(authenticationProvider())
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        if ("*".equals(allowedOrigins.trim())) {
            config.setAllowedOriginPatterns(List.of("*"));
        } else {
            config.setAllowedOrigins(Arrays.asList(allowedOrigins.split(",")));
        }
        config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"));
        config.setAllowedHeaders(List.of("*"));
        config.setAllowCredentials(true);
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        return source;
    }

    @Bean
    public AuthenticationProvider authenticationProvider() {
        DaoAuthenticationProvider provider = new DaoAuthenticationProvider();
        provider.setUserDetailsService(userDetailsService);
        provider.setPasswordEncoder(passwordEncoder());
        return provider;
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
