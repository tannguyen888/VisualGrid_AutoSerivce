package com.cardiag.obd.controller;

import com.cardiag.common.response.ApiResponse;
import com.cardiag.obd.dto.ObdRequest;
import com.cardiag.obd.dto.ObdResponse;
import com.cardiag.obd.service.ObdService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/obd")
@RequiredArgsConstructor
public class ObdController {

    private final ObdService obdService;

    @PostMapping("/execute")
    public ResponseEntity<ApiResponse<ObdResponse>> execute(@RequestBody ObdRequest request) {
        return ResponseEntity.ok(ApiResponse.success("OBD command executed", obdService.execute(request)));
    }
}
