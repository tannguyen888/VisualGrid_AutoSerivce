package com.cardiag.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class ObdResponse {
    private String vehicleVin;
    private String command;
    private String result;
}
