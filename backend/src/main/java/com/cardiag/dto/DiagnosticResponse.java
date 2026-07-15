package com.cardiag.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class DiagnosticResponse {
    private String code;
    private String description;
}
