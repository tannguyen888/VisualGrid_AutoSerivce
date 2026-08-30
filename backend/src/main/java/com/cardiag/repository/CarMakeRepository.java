package com.cardiag.repository;

import com.cardiag.model.CarMake;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface CarMakeRepository extends JpaRepository<CarMake, Long> {
    Optional<CarMake> findByNameIgnoreCase(String name);
}
