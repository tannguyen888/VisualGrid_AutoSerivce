package com.cardiag.controller;

import com.cardiag.response.ApiResponse;
import com.cardiag.service.CarApiSyncService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/carapi/sync")
@RequiredArgsConstructor
public class CarApiSyncController {

    private final CarApiSyncService carApiSyncService;

    @PostMapping("/years")
    public ResponseEntity<ApiResponse<Integer>> syncYears() {
        return ResponseEntity.ok(ApiResponse.success("Years synced", carApiSyncService.syncYears()));
    }

    @PostMapping("/makes")
    public ResponseEntity<ApiResponse<Integer>> syncMakes() {
        return ResponseEntity.ok(ApiResponse.success("Makes synced", carApiSyncService.syncMakes()));
    }

    @PostMapping("/models")
    public ResponseEntity<ApiResponse<Integer>> syncModels(@RequestParam Integer year, @RequestParam Long makeId) {
        return ResponseEntity.ok(ApiResponse.success("Models synced", carApiSyncService.syncModels(year, makeId)));
    }

    @PostMapping("/all")
    public ResponseEntity<ApiResponse<String>> syncAll() {
        carApiSyncService.syncAll();
        return ResponseEntity.ok(ApiResponse.success("Full sync triggered", "years + makes synced"));
    }
}
