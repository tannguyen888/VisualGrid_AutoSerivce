package com.cardiag.service;

import com.cardiag.config.CarApiProperties;
import com.cardiag.dto.carapi.CarApiLoginRequest;
import com.cardiag.dto.carapi.CarApiPageResponse;
import com.github.benmanes.caffeine.cache.Cache;
import lombok.RequiredArgsConstructor;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Component;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestClient;
import org.springframework.web.util.UriBuilder;

import java.net.URI;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

import static com.cardiag.config.CacheConfig.CARAPI_TOKEN_CACHE;

/**
 * Thin client around https://carapi.app. Caches the login JWT in a Caffeine
 * cache so a fresh token isn't requested on every single API call.
 */
@Component
@RequiredArgsConstructor
public class CarApiClient {

    private static final String TOKEN_KEY = "token";

    private final CarApiProperties properties;
    private final org.springframework.cache.CacheManager cacheManager;
    private final RestClient restClient = RestClient.builder().build();

    private String login() {
        // /api/auth/login returns the JWT as plain text (Content-Type: text/plain), not
        // JSON.
        String jwt = restClient.post()
                .uri(properties.getBaseUrl() + "/api/auth/login")
                .contentType(org.springframework.http.MediaType.APPLICATION_JSON)
                .body(new CarApiLoginRequest(properties.getApiToken(), properties.getApiSecret()))
                .retrieve()
                .body(String.class);
        return jwt == null ? "" : jwt.trim();
    }

    private String currentToken() {
        Cache cache = nativeCache();
        return (String) cache.get(TOKEN_KEY, key -> login());
    }

    private void invalidateToken() {
        nativeCache().invalidate(TOKEN_KEY);
    }

    @SuppressWarnings("unchecked")
    private Cache nativeCache() {
        return (Cache) cacheManager.getCache(CARAPI_TOKEN_CACHE).getNativeCache();
    }

    /**
     * GET a CarAPI endpoint using the {@code {"data": [...], "collection": {...}}}
     * envelope
     * (e.g. /api/makes/v2, /api/models/v2), retrying once with a refreshed token on
     * 401.
     */
    public <T> List<T> getList(String path, Map<String, Object> queryParams,
            ParameterizedTypeReference<CarApiPageResponse<T>> type) {
        try {
            CarApiPageResponse<T> response = doGet(path, queryParams, type, currentToken());
            return response == null || response.data() == null ? List.of() : response.data();
        } catch (HttpClientErrorException.Unauthorized e) {
            invalidateToken();
            CarApiPageResponse<T> response = doGet(path, queryParams, type, currentToken());
            return response == null || response.data() == null ? List.of() : response.data();
        }
    }

    /**
     * GET a CarAPI endpoint that returns a bare JSON array (e.g. /api/years/v2),
     * retrying once with a refreshed token on 401.
     */
    public <T> List<T> getArray(String path, Map<String, Object> queryParams,
            ParameterizedTypeReference<List<T>> type) {
        try {
            List<T> response = doGet(path, queryParams, type, currentToken());
            return response == null ? List.of() : response;
        } catch (HttpClientErrorException.Unauthorized e) {
            invalidateToken();
            List<T> response = doGet(path, queryParams, type, currentToken());
            return response == null ? List.of() : response;
        }
    }

    private <R> R doGet(String path, Map<String, Object> queryParams, ParameterizedTypeReference<R> type,
            String token) {
        Function<UriBuilder, URI> uriFn = builder -> {
            UriBuilder b = builder.path(path);
            queryParams.forEach((k, v) -> {
                if (v != null) {
                    b.queryParam(k, v);
                }
            });
            return b.build();
        };

        return restClient.get()
                .uri(properties.getBaseUrl(), uriFn)
                .headers(h -> h.setBearerAuth(token))
                .retrieve()
                .body(type);
    }
}
