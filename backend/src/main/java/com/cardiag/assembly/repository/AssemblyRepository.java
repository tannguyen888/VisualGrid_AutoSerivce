package com.cardiag.assembly.repository;

import com.cardiag.assembly.entity.Assembly;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AssemblyRepository extends JpaRepository<Assembly, Long> {
}
