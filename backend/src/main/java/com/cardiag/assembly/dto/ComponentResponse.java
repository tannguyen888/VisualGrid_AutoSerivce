package com.cardiag.assembly.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class ComponentResponse {
    private Long id;
    private String name;
    private String partNumber;
}
