package com.cardiag.repository;

import com.cardiag.model.DtcCode;
import org.springframework.data.jpa.repository.JpaRepository;

public interface DtcRepository extends JpaRepository<DtcCode, Long> {
}
