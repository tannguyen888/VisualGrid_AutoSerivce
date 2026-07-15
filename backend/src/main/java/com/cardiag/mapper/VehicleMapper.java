package com.cardiag.service;

import com.cardiag.dto.VehicleRequest;
import com.cardiag.dto.VehicleResponse;
import com.cardiag.model.Vehicle;

public final class VehicleMapper {

    private VehicleMapper() {
    }

    public static Vehicle toEntity(VehicleRequest request) {
        return Vehicle.builder()
                .vin(request.getVin())
                .make(request.getMake())
                .model(request.getModel())
                .year(request.getYear())
                .build();
    }

    public static VehicleResponse toResponse(Vehicle vehicle) {
        return VehicleResponse.builder()
                .id(vehicle.getId())
                .vin(vehicle.getVin())
                .make(vehicle.getMake())
                .model(vehicle.getModel())
                .year(vehicle.getYear())
                .build();
    }
}
