package com.cardiag.repository;

import com.cardiag.model.RepairProcedure;
import org.springframework.data.jpa.repository.JpaRepository;

public interface RepairRepository extends JpaRepository<RepairProcedure, Long> {
}
