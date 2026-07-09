package com.cardiag.obd.dto;

import lombok.Data;

@Data
public class ObdRequest {
    private String vehicleVin;
    private String command;
}
