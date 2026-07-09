package com.cardiag.vehicle.service;

import com.cardiag.vehicle.dto.VehicleRequest;
import com.cardiag.vehicle.dto.VehicleResponse;
import com.cardiag.vehicle.entity.Vehicle;

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
