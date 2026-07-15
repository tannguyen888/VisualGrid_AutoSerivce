package com.cardiag.service;

import com.cardiag.dto.DiagnosticResponse;
import com.cardiag.model.DtcCode;
import com.cardiag.repository.DtcRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class DiagnosticService {

    private final DtcRepository dtcRepository;

    public List<DiagnosticResponse> findAll() {
        return dtcRepository.findAll().stream().map(this::toResponse).toList();
    }

    private DiagnosticResponse toResponse(DtcCode dtcCode) {
        return DiagnosticResponse.builder()
                .code(dtcCode.getCode())
                .description(dtcCode.getDescription())
                .build();
    }
}
