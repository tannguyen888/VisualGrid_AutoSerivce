package com.cardiag.dto.carapi;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = true)
public record CarApiTrimDto(
        Long id,
        String name,
        @JsonProperty("make_model_id") Long modelId,
        @JsonProperty("make") String makeName,
        @JsonProperty("model") String modelName,
        Integer year) {
}
