package com.cardiag.dto.ai;

import lombok.Builder;

import java.util.List;

/**
 * Context AI_service fetches before generating a diagnosis/repair procedure.
 */
@Builder
public record AiContextResponse(
        String code,
        String dtcDescription,
        String make,
        String model,
        String trim,
        Integer year,
        List<RepairProcedureResponse> existingProcedures) {
}
