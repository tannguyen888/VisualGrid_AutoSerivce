package com.cardiag.common.response;

public record ApiResponse(
        boolean success,
        String data) {

    public static ApiResponse of(String data) throws IllegalArgumentException {
        if (data == null || data.isEmpty()) {
            throw new IllegalArgumentException("Data cannot be null or empty");
        }
        return new ApiResponse(true, data);
    }
}
