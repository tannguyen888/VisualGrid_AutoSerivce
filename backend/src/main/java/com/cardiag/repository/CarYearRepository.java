package com.cardiag.repository;

import com.cardiag.model.CarYear;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CarYearRepository extends JpaRepository<CarYear, Integer> {
}
