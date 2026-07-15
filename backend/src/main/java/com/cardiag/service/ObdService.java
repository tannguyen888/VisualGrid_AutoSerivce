package com.cardiag.service;

import com.cardiag.dto.ObdRequest;
import com.cardiag.dto.ObdResponse;
import org.springframework.stereotype.Service;

@Service
public class ObdService {

    public ObdResponse execute(ObdRequest request) {
        return ObdResponse.builder()
                .vehicleVin(request.getVehicleVin())
                .command(request.getCommand())
                .result("Simulated OBD response")
                .build();
    }
}
