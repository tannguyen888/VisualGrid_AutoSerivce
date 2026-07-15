package com.cardiag.service;

import com.cardiag.dto.AssemblyResponse;
import com.cardiag.model.Assembly;
import com.cardiag.repository.AssemblyRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class AssemblyService {

    private final AssemblyRepository assemblyRepository;

    public List<AssemblyResponse> findAll() {
        return assemblyRepository.findAll().stream().map(this::toResponse).toList();
    }

    private AssemblyResponse toResponse(Assembly assembly) {
        return AssemblyResponse.builder()
                .id(assembly.getId())
                .code(assembly.getCode())
                .name(assembly.getName())
                .components(List.of())
                .build();
    }
}
