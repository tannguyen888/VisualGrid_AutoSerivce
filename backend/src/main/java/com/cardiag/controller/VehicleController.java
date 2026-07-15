package com.cardiag.controller;

import com.cardiag.response.ApiResponse;
import com.cardiag.dto.VehicleRequest;
import com.cardiag.dto.VehicleResponse;
import com.cardiag.service.VehicleService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/vehicles")
@RequiredArgsConstructor
public class VehicleController {

    private final VehicleService vehicleService;

    @PostMapping
    public ResponseEntity<ApiResponse<VehicleResponse>> create(@RequestBody VehicleRequest request) {
        return ResponseEntity.ok(ApiResponse.success("Vehicle created", vehicleService.create(request)));
    }

    @GetMapping
    public ResponseEntity<ApiResponse<List<VehicleResponse>>> findAll() {
        return ResponseEntity.ok(ApiResponse.success("Vehicles fetched", vehicleService.findAll()));
    }
}
