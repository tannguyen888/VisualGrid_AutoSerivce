package com.cardiag.repository;

import com.cardiag.model.CarTrim;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface CarTrimRepository extends JpaRepository<CarTrim, Long> {
    Optional<CarTrim> findFirstByNameIgnoreCaseAndModelNameIgnoreCase(String name, String modelName);
}
