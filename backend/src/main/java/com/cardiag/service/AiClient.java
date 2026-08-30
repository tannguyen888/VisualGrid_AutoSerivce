package com.cardiag.service;

import com.cardiag.config.AiProperties;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class AiClient {

    private final AiProperties aiProperties;

    public String analyze(String prompt) {
        // aiProperties.getApiKey() is read from application.properties (gitignored,
        // local secrets)
        return "AI analysis placeholder for: " + prompt;
    }
}
