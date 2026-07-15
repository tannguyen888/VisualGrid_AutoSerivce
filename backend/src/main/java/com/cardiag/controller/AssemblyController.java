package com.cardiag.controller;

import com.cardiag.dto.AssemblyResponse;
import com.cardiag.service.AssemblyService;
import com.cardiag.response.ApiResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/assemblies")
@RequiredArgsConstructor
public class AssemblyController {

    private final AssemblyService assemblyService;

    @GetMapping
    public ResponseEntity<ApiResponse<List<AssemblyResponse>>> findAll() {
        return ResponseEntity.ok(ApiResponse.success("Assemblies fetched", assemblyService.findAll()));
    }
}
