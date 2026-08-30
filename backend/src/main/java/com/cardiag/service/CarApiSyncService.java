package com.cardiag.service;

import com.cardiag.config.CarApiProperties;
import com.cardiag.dto.carapi.CarApiMakeDto;
import com.cardiag.dto.carapi.CarApiModelDto;
import com.cardiag.dto.carapi.CarApiPageResponse;
import com.cardiag.model.CarMake;
import com.cardiag.model.CarModel;
import com.cardiag.model.CarYear;
import com.cardiag.repository.CarMakeRepository;
import com.cardiag.repository.CarModelRepository;
import com.cardiag.repository.CarYearRepository;
import com.github.benmanes.caffeine.cache.Cache;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.CacheManager;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import static com.cardiag.config.CacheConfig.CARAPI_MAKE_EXISTS_CACHE;
import static com.cardiag.config.CacheConfig.CARAPI_MODEL_EXISTS_CACHE;

/**
 * Pulls reference data (years/makes/models) from CarAPI and feeds it into the
 * local database. Existence checks are cached in-memory with Caffeine so a
 * bulk parse doesn't fire a "SELECT exists" for every single row - the DB is
 * only hit for rows actually missing, and writes go in batches via saveAll().
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class CarApiSyncService {

    private final CarApiClient carApiClient;
    private final CarApiProperties properties;
    private final CacheManager cacheManager;

    private final CarYearRepository carYearRepository;
    private final CarMakeRepository carMakeRepository;
    private final CarModelRepository carModelRepository;

    public int syncYears() {
        List<Integer> years = carApiClient.getArray("/api/years/v2", Map.of(),
                new ParameterizedTypeReference<List<Integer>>() {
                });

        List<CarYear> toSave = years.stream()
                .filter(y -> !carYearRepository.existsById(y))
                .map(y -> CarYear.builder().year(y).build())
                .toList();

        carYearRepository.saveAll(toSave);
        return toSave.size();
    }

    public int syncMakes() {
        List<CarApiMakeDto> makes = carApiClient.getList("/api/makes/v2", Map.of(),
                new ParameterizedTypeReference<CarApiPageResponse<CarApiMakeDto>>() {
                });

        Cache existsCache = nativeCache(CARAPI_MAKE_EXISTS_CACHE);
        int batchSize = properties.getSync().getBatchSize();
        List<CarMake> batch = new ArrayList<>(batchSize);
        int saved = 0;

        for (CarApiMakeDto dto : makes) {
            if (dto.id() == null) {
                continue;
            }
            boolean alreadyKnown = Boolean.TRUE
                    .equals(existsCache.get(dto.id(), id -> carMakeRepository.existsById((Long) id)));
            if (alreadyKnown) {
                continue;
            }
            batch.add(CarMake.builder().id(dto.id()).name(dto.name()).build());
            existsCache.put(dto.id(), true);
            if (batch.size() >= batchSize) {
                carMakeRepository.saveAll(batch);
                saved += batch.size();
                batch.clear();
            }
        }
        if (!batch.isEmpty()) {
            carMakeRepository.saveAll(batch);
            saved += batch.size();
        }
        return saved;
    }

    public int syncModels(Integer year, Long makeId) {
        List<CarApiModelDto> models = carApiClient.getList("/api/models/v2",
                Map.of("year", year, "make_id", makeId),
                new ParameterizedTypeReference<CarApiPageResponse<CarApiModelDto>>() {
                });

        Cache existsCache = nativeCache(CARAPI_MODEL_EXISTS_CACHE);
        int batchSize = properties.getSync().getBatchSize();
        List<CarModel> batch = new ArrayList<>(batchSize);
        int saved = 0;

        for (CarApiModelDto dto : models) {
            if (dto.id() == null) {
                continue;
            }
            boolean alreadyKnown = Boolean.TRUE
                    .equals(existsCache.get(dto.id(), id -> carModelRepository.existsById((Long) id)));
            if (alreadyKnown) {
                continue;
            }
            batch.add(CarModel.builder()
                    .id(dto.id())
                    .name(dto.name())
                    .makeId(dto.makeId())
                    .makeName(dto.makeName())
                    .year(year)
                    .build());
            existsCache.put(dto.id(), true);
            if (batch.size() >= batchSize) {
                carModelRepository.saveAll(batch);
                saved += batch.size();
                batch.clear();
            }
        }
        if (!batch.isEmpty()) {
            carModelRepository.saveAll(batch);
            saved += batch.size();
        }
        return saved;
    }

    /**
     * Syncs the lightweight reference data only (years + makes). Model/trim sync is
     * on-demand per make/year.
     */
    public void syncAll() {
        int years = syncYears();
        int makes = syncMakes();
        log.info("CarAPI sync complete: {} years, {} makes", years, makes);
    }

    private Cache nativeCache(String name) {
        return (Cache) cacheManager.getCache(name).getNativeCache();
    }
}
