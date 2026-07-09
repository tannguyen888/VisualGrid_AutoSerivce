package com.cardiag.vehicle.service;

import com.cardiag.vehicle.dto.VehicleRequest;
import com.cardiag.vehicle.dto.VehicleResponse;

import java.util.List;

public interface VehicleService {
    VehicleResponse create(VehicleRequest request);
    List<VehicleResponse> findAll();
}
