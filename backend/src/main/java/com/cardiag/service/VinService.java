package com.cardiag.service;

import com.cardiag.service.VinApiClient;
import com.cardiag.dto.VinResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class VinService {

    private final VinApiClient vinApiClient;

    public VinResponse decode(String vin) {
        return vinApiClient.decodeVin(vin);
    }
}
