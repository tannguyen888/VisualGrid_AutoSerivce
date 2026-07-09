package com.cardiag.vin.service;

import com.cardiag.vin.client.VinApiClient;
import com.cardiag.vin.dto.VinResponse;
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
