package com.cardiag.dto.carapi;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public record CarApiLoginRequest(String api_token, String api_secret) {
}
