package com.cardiag.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class VinResponse {
    private String vin;
    private String make;
    private String model;
    private Integer year;
}
