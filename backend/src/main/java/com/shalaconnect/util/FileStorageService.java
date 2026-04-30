package com.shalaconnect.util;

import com.shalaconnect.exception.BadRequestException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.*;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;

@Service
public class FileStorageService {

    @Value("${app.upload.dir:uploads}")
    private String uploadDir;

    private static final List<String> ALLOWED_IMAGE_TYPES = Arrays.asList(
        "image/jpeg", "image/jpg", "image/png", "image/webp"
    );
    private static final List<String> ALLOWED_DOC_TYPES = Arrays.asList(
        "application/pdf", "image/jpeg", "image/jpg", "image/png"
    );

    public String storeFile(MultipartFile file, String subDir) {
        String originalFilename = StringUtils.cleanPath(
            file.getOriginalFilename() != null ? file.getOriginalFilename() : "file"
        );
        String extension = "";
        int dotIndex = originalFilename.lastIndexOf('.');
        if (dotIndex >= 0) extension = originalFilename.substring(dotIndex);

        String newFilename = UUID.randomUUID().toString() + extension;
        Path targetDir = Paths.get(uploadDir, subDir).toAbsolutePath().normalize();

        try {
            Files.createDirectories(targetDir);
            Path targetPath = targetDir.resolve(newFilename);
            Files.copy(file.getInputStream(), targetPath, StandardCopyOption.REPLACE_EXISTING);
            return subDir + "/" + newFilename;
        } catch (IOException ex) {
            throw new BadRequestException("Failed to store file: " + ex.getMessage());
        }
    }

    public void deleteFile(String filePath) {
        if (filePath == null || filePath.isBlank()) return;
        try {
            Path path = Paths.get(uploadDir, filePath).toAbsolutePath().normalize();
            Files.deleteIfExists(path);
        } catch (IOException ignored) {}
    }

    public void validateImageFile(MultipartFile file) {
        if (file == null || file.isEmpty()) throw new BadRequestException("File is empty");
        if (!ALLOWED_IMAGE_TYPES.contains(file.getContentType()))
            throw new BadRequestException("Only JPEG, PNG, and WebP images are allowed");
    }

    public void validateDocumentFile(MultipartFile file) {
        if (file == null || file.isEmpty()) throw new BadRequestException("File is empty");
        if (!ALLOWED_DOC_TYPES.contains(file.getContentType()))
            throw new BadRequestException("Only PDF and image files are allowed");
    }

    public Path getFilePath(String relativePath) {
        return Paths.get(uploadDir, relativePath).toAbsolutePath().normalize();
    }
}
