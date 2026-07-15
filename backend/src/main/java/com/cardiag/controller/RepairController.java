package com.cardiag.controller;

import com.cardiag.response.ApiResponse;
import com.cardiag.dto.RepairResponse;
import com.cardiag.service.RepairService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/repairs")
@RequiredArgsConstructor
public class RepairController {

    private final RepairService repairService;

    @GetMapping
    public ResponseEntity<ApiResponse<List<RepairResponse>>> findAll() {
        return ResponseEntity.ok(ApiResponse.success("Repairs fetched", repairService.findAll()));
    }
}
