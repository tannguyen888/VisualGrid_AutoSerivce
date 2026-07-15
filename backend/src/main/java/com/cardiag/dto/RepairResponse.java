package com.cardiag.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class RepairResponse {
    private Long id;
    private String title;
    private String steps;
}
