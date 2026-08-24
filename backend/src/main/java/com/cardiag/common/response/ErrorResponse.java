package com.cardiag.common.response;

import java.time.LocalDateTime;
import java.util.Map;

public record ErrorResponse(

        boolean success,

        String code,

        String message,

        LocalDateTime timestamp,

        Map<String, String> errors

) {

    public static ErrorResponse of(
            String code,
            String message) {

        return new ErrorResponse(
                false,
                code,
                message,
                LocalDateTime.now(),
                null);
    }

    public static ErrorResponse validation(
            Map<String, String> errors) {

        return new ErrorResponse(
                false,
                "VALIDATION_ERROR",
                "Validation failed",
                LocalDateTime.now(),
                errors);
    }
}