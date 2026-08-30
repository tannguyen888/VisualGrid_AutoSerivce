package com.cardiag.dto.carapi;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public record CarApiMakeDto(Long id, String name) {
}
