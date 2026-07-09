package com.cardiag.vehicle.repository;

import com.cardiag.vehicle.entity.Engine;
import org.springframework.data.jpa.repository.JpaRepository;

public interface EngineRepository extends JpaRepository<Engine, Long> {
}
