package com.cardiag.repair.repository;

import com.cardiag.repair.entity.RepairProcedure;
import org.springframework.data.jpa.repository.JpaRepository;

public interface RepairRepository extends JpaRepository<RepairProcedure, Long> {
}
