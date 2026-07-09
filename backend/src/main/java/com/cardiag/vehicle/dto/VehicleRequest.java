package com.cardiag.vehicle.dto;

import lombok.Data;

@Data
public class VehicleRequest {
    private String vin;
    private String make;
    private String model;
    private Integer year;
}
