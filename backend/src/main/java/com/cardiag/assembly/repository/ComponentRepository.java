package com.cardiag.assembly.repository;

import com.cardiag.assembly.entity.Component;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ComponentRepository extends JpaRepository<Component, Long> {
}
