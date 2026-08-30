package com.cardiag.common.exception;

import com.cardiag.common.response.ErrorResponse;
import com.cardiag.exception.BusinessException;

import jakarta.validation.ConstraintViolationException;

import org.springframework.dao.DataIntegrityViolationException;

import org.springframework.http.HttpStatus;

import org.springframework.http.ResponseEntity;

import org.springframework.web.bind.MethodArgumentNotValidException;

import org.springframework.web.bind.annotation.ExceptionHandler;

import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.HashMap;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {

        @ExceptionHandler(ResourcesNotFound.class)
        public ResponseEntity<ErrorResponse> handleResourceNotFound(
                        ResourcesNotFound ex) {

                ErrorResponse response = ErrorResponse.of(
                                ErrorConstants.RESOURCE_NOT_FOUND.name(),
                                ex.getMessage());

                return ResponseEntity
                                .status(HttpStatus.NOT_FOUND)
                                .body(response);
        }

        @ExceptionHandler(BadRequestHandler.class)
        public ResponseEntity<ErrorResponse> handleBadRequest(
                        BadRequestHandler ex) {

                ErrorResponse response = ErrorResponse.of(
                                ErrorConstants.BAD_REQUEST.name(),
                                ex.getMessage());

                return ResponseEntity
                                .status(HttpStatus.BAD_REQUEST)
                                .body(response);
        }

        @ExceptionHandler(BusinessException.class)
        public ResponseEntity<ErrorResponse> handleBusinessException(BusinessException ex) {

                ErrorResponse response = ErrorResponse.of(
                                ErrorConstants.BAD_REQUEST.name(),
                                ex.getMessage());

                return ResponseEntity
                                .status(HttpStatus.BAD_REQUEST)
                                .body(response);
        }

        @ExceptionHandler(MethodArgumentNotValidException.class)
        public ResponseEntity<ErrorResponse> handleValidation(
                        MethodArgumentNotValidException ex) {

                Map<String, String> errors = new HashMap<>();

                ex.getBindingResult()
                                .getFieldErrors()
                                .forEach(error -> errors.put(
                                                error.getField(),
                                                error.getDefaultMessage()));

                return ResponseEntity
                                .status(HttpStatus.BAD_REQUEST)
                                .body(
                                                ErrorResponse.validation(errors));
        }

        @ExceptionHandler(ConstraintViolationException.class)
        public ResponseEntity<ErrorResponse> handleConstraintViolation(
                        ConstraintViolationException ex) {

                ErrorResponse response = ErrorResponse.of(
                                ErrorConstants.VALIDATION_ERROR.name(),
                                ex.getMessage());

                return ResponseEntity
                                .status(HttpStatus.BAD_REQUEST)
                                .body(response);
        }

        @ExceptionHandler(DataIntegrityViolationException.class)
        public ResponseEntity<ErrorResponse> handleDataIntegrity(
                        DataIntegrityViolationException ex) {

                ErrorResponse response = ErrorResponse.of(
                                ErrorConstants.DATA_INTEGRITY_ERROR.name(),
                                "Database constraint violation");

                return ResponseEntity
                                .status(HttpStatus.CONFLICT)
                                .body(response);
        }

        @ExceptionHandler(ExternalServiceException.class)
        public ResponseEntity<ErrorResponse> handleExternalService(
                        ExternalServiceException ex) {

                ErrorResponse response = ErrorResponse.of(
                                ErrorConstants.EXTERNAL_SERVICE_ERROR.name(),
                                "External service is unavailable");

                return ResponseEntity
                                .status(HttpStatus.BAD_GATEWAY)
                                .body(response);
        }

        @ExceptionHandler(Exception.class)
        public ResponseEntity<ErrorResponse> handleUnknown(Exception ex) {

                ex.printStackTrace();

                ErrorResponse response = ErrorResponse.of(
                                ErrorConstants.INTERNAL_SERVER_ERROR.name(),
                                "An unexpected error occurred");

                return ResponseEntity
                                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                                .body(response);
        }
}