package com.cardiag.config;

import com.cardiag.service.CarApiSyncService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Optionally kicks off a CarAPI reference-data sync after the application
 * context is up. Runs off the main thread and behind a feature flag
 * (carapi.sync.on-startup) so it never blocks/slows down boot.
 */
@Slf4j
@Configuration
@RequiredArgsConstructor
public class CarApiStartupConfig {

    private final CarApiProperties properties;
    private final CarApiSyncService carApiSyncService;

    @Bean
    public ApplicationRunner carApiStartupSyncRunner() {
        return (ApplicationArguments args) -> {
            if (!properties.getSync().isOnStartup()) {
                return;
            }
            Thread.ofVirtual().name("carapi-startup-sync").start(() -> {
                try {
                    carApiSyncService.syncAll();
                } catch (Exception e) {
                    log.warn("CarAPI startup sync failed", e);
                }
            });
        };
    }
}
