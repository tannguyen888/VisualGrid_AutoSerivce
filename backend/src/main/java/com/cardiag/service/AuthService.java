package com.cardiag.service;

import com.cardiag.dto.AuthResponse;
import com.cardiag.dto.LoginRequest;
import com.cardiag.dto.RegisterRequest;

public interface AuthService {
    AuthResponse login(LoginRequest request);
    AuthResponse register(RegisterRequest request);
}
