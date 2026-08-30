package com.cardiag.config;

import com.github.benmanes.caffeine.cache.Caffeine;
import org.springframework.cache.CacheManager;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.cache.caffeine.CaffeineCacheManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.concurrent.TimeUnit;

/**
 * Caffeine caches used to avoid hammering Postgres while CarAPI reference
 * data (years/makes/models/trims) is parsed in bulk on startup or on demand.
 */
@Configuration
@EnableCaching
public class CacheConfig {

    public static final String CARAPI_TOKEN_CACHE = "carApiToken";
    public static final String CARAPI_MAKE_EXISTS_CACHE = "carApiMakeExists";
    public static final String CARAPI_MODEL_EXISTS_CACHE = "carApiModelExists";
    public static final String CARAPI_TRIM_EXISTS_CACHE = "carApiTrimExists";

    @Bean
    public CacheManager cacheManager() {
        CaffeineCacheManager manager = new CaffeineCacheManager(
                CARAPI_TOKEN_CACHE,
                CARAPI_MAKE_EXISTS_CACHE,
                CARAPI_MODEL_EXISTS_CACHE,
                CARAPI_TRIM_EXISTS_CACHE);
        manager.setCaffeine(Caffeine.newBuilder()
                .maximumSize(50_000)
                .expireAfterWrite(30, TimeUnit.MINUTES));
        return manager;
    }
}
