package com.cardiag.dto.carapi;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/**
 * CarAPI list response envelope, e.g. for /api/makes/v2 and /api/models/v2:
 * {"data": [...], "collection":
 * {"url":"...","count":50,"pages":20,"total":200,"next":"...","prev":"...","first":"...","last":"..."}}
 * Note: /api/years/v2 does NOT use this envelope, it returns a bare JSON array.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
public record CarApiPageResponse<T>(java.util.List<T> data, Collection collection) {

    @JsonIgnoreProperties(ignoreUnknown = true)
    public record Collection(String url, Integer count, Integer pages, Integer total, String next, String prev) {
    }
}
