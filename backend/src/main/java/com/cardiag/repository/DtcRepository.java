package com.cardiag.repository;

import com.cardiag.model.DtcCode;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface DtcRepository extends JpaRepository<DtcCode, Long> {
    Optional<DtcCode> findByCodeIgnoreCase(String code);
}
