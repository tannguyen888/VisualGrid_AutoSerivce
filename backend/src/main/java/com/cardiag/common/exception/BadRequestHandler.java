package com.cardiag.common.exception;

public class BadRequestHandler extends RuntimeException {
    public BadRequestHandler(String message) {
        super(message);
    }

}
