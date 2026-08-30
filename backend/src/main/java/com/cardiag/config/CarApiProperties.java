package com.cardiag.config;

import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Getter
@Setter
@Component
@ConfigurationProperties(prefix = "carapi")
public class CarApiProperties {

    private String baseUrl;
    private String apiToken;
    private String apiSecret;
    private Sync sync = new Sync();

    @Getter
    @Setter
    public static class Sync {
        private int batchSize = 200;
        private boolean onStartup = false;
    }
}
