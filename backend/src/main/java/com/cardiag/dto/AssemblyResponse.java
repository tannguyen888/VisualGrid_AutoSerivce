package com.cardiag.dto;

import lombok.Builder;
import lombok.Data;

import java.util.List;

@Data
@Builder
public class AssemblyResponse {
    private Long id;
    private String code;
    private String name;
    private List<ComponentResponse> components;
}
