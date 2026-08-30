package com.cardiag.dto.carapi;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = true)
public record CarApiModelDto(
        Long id,
        String name,
        @JsonProperty("make_id") Long makeId,
        @JsonProperty("make") String makeName,
        Integer year) {
}
