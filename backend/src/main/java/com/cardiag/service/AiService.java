package com.cardiag.service;

import com.cardiag.service.AiClient;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AiService {

    private final AiClient aiClient;

    public String analyzeDiagnostic(String input) {
        return aiClient.analyze(input);
    }
}
