package com.cardiag.repository;

import com.cardiag.model.Tool;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface ToolRepository extends JpaRepository<Tool, Long> {
    Optional<Tool> findByNameIgnoreCase(String name);
}
