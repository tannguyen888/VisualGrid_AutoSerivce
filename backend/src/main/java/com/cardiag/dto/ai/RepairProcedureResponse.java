package com.cardiag.dto.ai;

import lombok.Builder;

import java.util.List;

@Builder
public record RepairProcedureResponse(
        Long id,
        String dtcCode,
        String vehicleMake,
        String vehicleModel,
        String vehicleTrim,
        Integer vehicleYear,
        String title,
        String steps,
        List<String> parts,
        List<String> tools) {
}
