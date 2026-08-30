package com.cardiag.repository;

import com.cardiag.model.RepairProcedure;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface RepairRepository extends JpaRepository<RepairProcedure, Long> {
    List<RepairProcedure> findByDtcCodeIgnoreCase(String dtcCode);
}
