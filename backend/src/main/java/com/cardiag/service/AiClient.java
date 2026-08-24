package com.cardiag.service;

import org.springframework.stereotype.Component;

@Component
public class AiClient {

    public String analyze(String prompt) {
        return "AI analysis placeholder for: " + prompt;
    }
}
