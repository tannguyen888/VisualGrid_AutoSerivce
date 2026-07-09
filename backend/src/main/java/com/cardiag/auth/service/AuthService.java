package com.cardiag.auth.service;

import com.cardiag.auth.dto.AuthResponse;
import com.cardiag.auth.dto.LoginRequest;
import com.cardiag.auth.dto.RegisterRequest;

public interface AuthService {
    AuthResponse login(LoginRequest request);
    AuthResponse register(RegisterRequest request);
}
