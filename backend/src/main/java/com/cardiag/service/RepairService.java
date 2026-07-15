package com.cardiag.service;

import com.cardiag.dto.RepairResponse;
import com.cardiag.model.RepairProcedure;
import com.cardiag.repository.RepairRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class RepairService {

    private final RepairRepository repairRepository;

    public List<RepairResponse> findAll() {
        return repairRepository.findAll().stream().map(this::toResponse).toList();
    }

    private RepairResponse toResponse(RepairProcedure p) {
        return RepairResponse.builder()
                .id(p.getId())
                .title(p.getTitle())
                .steps(p.getSteps())
                .build();
    }
}
