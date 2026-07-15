package com.cardiag.service;

import com.cardiag.dto.VehicleRequest;
import com.cardiag.dto.VehicleResponse;

import java.util.List;

public interface VehicleService {
    VehicleResponse create(VehicleRequest request);
    List<VehicleResponse> findAll();
}
