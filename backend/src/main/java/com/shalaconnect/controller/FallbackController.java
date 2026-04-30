package com.shalaconnect.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.FileSystemResource;
import org.springframework.core.io.Resource;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.nio.file.Paths;

@RestController
public class FallbackController {

    @Value("${app.static.dir:static}")
    private String staticDir;

    @GetMapping(value = {"/{path:[^\\.]*}", "/{path:[^\\.]*}/**"})
    public ResponseEntity<Resource> forward() {
        Resource resource = new FileSystemResource(
            Paths.get(staticDir).toAbsolutePath().normalize().resolve("index.html").toFile()
        );
        return ResponseEntity.ok().contentType(MediaType.TEXT_HTML).body(resource);
    }
}
