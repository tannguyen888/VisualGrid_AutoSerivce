package com.cardiag.diagnostic.controller;

import com.cardiag.common.response.ApiResponse;
import com.cardiag.diagnostic.dto.DiagnosticResponse;
import com.cardiag.diagnostic.service.DiagnosticService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/diagnostics")
@RequiredArgsConstructor
public class DiagnosticController {

    private final DiagnosticService diagnosticService;

    @GetMapping
    public ResponseEntity<ApiResponse<List<DiagnosticResponse>>> findAll() {
        return ResponseEntity.ok(ApiResponse.success("Diagnostics fetched", diagnosticService.findAll()));
    }
}
