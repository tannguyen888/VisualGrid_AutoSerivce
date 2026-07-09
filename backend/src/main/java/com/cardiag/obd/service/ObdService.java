package com.cardiag.obd.service;

import com.cardiag.obd.dto.ObdRequest;
import com.cardiag.obd.dto.ObdResponse;
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
