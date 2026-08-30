package com.cardiag.dto.ai;

import java.util.List;

/**
 * Payload AI_service sends back after generating a repair procedure for a DTC +
 * vehicle.
 */
public record RepairProcedureRequest(
        String dtcCode,
        String vehicleMake,
        String vehicleModel,
        String vehicleTrim,
        Integer vehicleYear,
        String title,
        String steps,
        List<PartRequest> parts,
        List<ToolRequest> tools) {
}
