package com.cardiag.diagnostic.repository;

import com.cardiag.diagnostic.entity.DtcCode;
import org.springframework.data.jpa.repository.JpaRepository;

public interface DtcRepository extends JpaRepository<DtcCode, Long> {
}
