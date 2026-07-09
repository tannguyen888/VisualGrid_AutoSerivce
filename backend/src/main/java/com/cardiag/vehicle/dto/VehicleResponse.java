package com.cardiag.vehicle.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class VehicleResponse {
    private Long id;
    private String vin;
    private String make;
    private String model;
    private Integer year;
}
