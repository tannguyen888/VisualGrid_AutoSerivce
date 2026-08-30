package com.cardiag.controller;

import com.cardiag.dto.ai.AiContextResponse;
import com.cardiag.dto.ai.RepairProcedureRequest;
import com.cardiag.dto.ai.RepairProcedureResponse;
import com.cardiag.response.ApiResponse;
import com.cardiag.service.AiIntegrationService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * Machine-to-machine endpoints for AI_service, protected by
 * InternalApiKeyFilter (see SecurityConfig).
 */
@RestController
@RequestMapping("/api/ai")
@RequiredArgsConstructor
public class AiIntegrationController {

    private final AiIntegrationService aiIntegrationService;

    @GetMapping("/context")
    public ResponseEntity<ApiResponse<AiContextResponse>> getContext(
            @RequestParam String code,
            @RequestParam(required = false) String make,
            @RequestParam(required = false) String model,
            @RequestParam(required = false) String trim,
            @RequestParam(required = false) Integer year) {
        return ResponseEntity.ok(ApiResponse.success("Context fetched",
                aiIntegrationService.getContext(code, make, model, trim, year)));
    }

    @PostMapping("/repairs")
    public ResponseEntity<ApiResponse<RepairProcedureResponse>> saveRepairProcedure(
            @RequestBody RepairProcedureRequest request) {
        return ResponseEntity.ok(ApiResponse.success("Repair procedure saved",
                aiIntegrationService.saveRepairProcedure(request)));
    }
}
