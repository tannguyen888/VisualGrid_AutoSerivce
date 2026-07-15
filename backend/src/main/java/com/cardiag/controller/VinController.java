package com.cardiag.controller;

import com.cardiag.response.ApiResponse;
import com.cardiag.dto.VinResponse;
import com.cardiag.service.VinService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/vin")
@RequiredArgsConstructor
public class VinController {

    private final VinService vinService;

    @GetMapping("/decode")
    public ResponseEntity<ApiResponse<VinResponse>> decode(@RequestParam String vin) {
        return ResponseEntity.ok(ApiResponse.success("VIN decoded", vinService.decode(vin)));
    }
}
