package com.cardiag.vin.client;

import com.cardiag.vin.dto.VinResponse;
import org.springframework.stereotype.Component;

@Component
public class VinApiClient {

    public VinResponse decodeVin(String vin) {
        return VinResponse.builder()
                .vin(vin)
                .make("Unknown")
                .model("Unknown")
                .year(0)
                .build();
    }
}
