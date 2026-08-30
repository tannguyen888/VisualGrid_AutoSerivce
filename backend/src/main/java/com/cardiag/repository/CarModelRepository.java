package com.cardiag.repository;

import com.cardiag.model.CarModel;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface CarModelRepository extends JpaRepository<CarModel, Long> {
    Optional<CarModel> findFirstByNameIgnoreCaseAndMakeNameIgnoreCase(String name, String makeName);
}
