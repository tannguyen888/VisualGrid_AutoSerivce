package com.cardiag.config;

import java.time.LocalDateTime;
import java.time.ZoneOffset;

public final class DateUtils {

    private DateUtils() {
    }

    public static long toEpochMillis(LocalDateTime dateTime) {
        return dateTime.toInstant(ZoneOffset.UTC).toEpochMilli();
    }
}
