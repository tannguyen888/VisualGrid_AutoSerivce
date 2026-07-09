package com.cardiag.vehicle.service;

import com.cardiag.vehicle.dto.VehicleRequest;
import com.cardiag.vehicle.dto.VehicleResponse;
import com.cardiag.vehicle.entity.Vehicle;
import com.cardiag.vehicle.repository.VehicleRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class VehicleServiceImpl implements VehicleService {

    private final VehicleRepository vehicleRepository;

    @Override
    public VehicleResponse create(VehicleRequest request) {
        Vehicle saved = vehicleRepository.save(VehicleMapper.toEntity(request));
        return VehicleMapper.toResponse(saved);
    }

    @Override
    public List<VehicleResponse> findAll() {
        return vehicleRepository.findAll().stream().map(VehicleMapper::toResponse).toList();
    }
}
