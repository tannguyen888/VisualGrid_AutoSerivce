package com.cardiag.config;

import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Getter
@Setter
@Component
@ConfigurationProperties(prefix = "ai")
public class AiProperties {

    private String apiKey;

    /**
     * Shared secret AI_service must send as X-Internal-Api-Key to call /api/ai/**.
     */
    private String backendApiKey;
}
