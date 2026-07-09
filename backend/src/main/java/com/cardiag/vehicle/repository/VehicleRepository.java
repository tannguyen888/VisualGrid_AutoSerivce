package com.cardiag.vehicle.repository;

import com.cardiag.vehicle.entity.Vehicle;
import org.springframework.data.jpa.repository.JpaRepository;

public interface VehicleRepository extends JpaRepository<Vehicle, Long> {
}
