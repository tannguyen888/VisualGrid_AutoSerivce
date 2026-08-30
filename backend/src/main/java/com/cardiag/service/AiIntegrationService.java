package com.cardiag.service;

import com.cardiag.dto.ai.AiContextResponse;
import com.cardiag.dto.ai.PartRequest;
import com.cardiag.dto.ai.RepairProcedureRequest;
import com.cardiag.dto.ai.RepairProcedureResponse;
import com.cardiag.dto.ai.ToolRequest;
import com.cardiag.model.DtcCode;
import com.cardiag.model.Part;
import com.cardiag.model.RepairProcedure;
import com.cardiag.model.Tool;
import com.cardiag.repository.CarMakeRepository;
import com.cardiag.repository.CarModelRepository;
import com.cardiag.repository.CarTrimRepository;
import com.cardiag.repository.DtcRepository;
import com.cardiag.repository.PartRepository;
import com.cardiag.repository.RepairRepository;
import com.cardiag.repository.ToolRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

/**
 * Bridges AI_service to the vehicle/DTC reference data and repair procedures
 * stored by the Java backend: AI_service reads context here before generating
 * a diagnosis, then writes the generated repair procedure back via this
 * service.
 */
@Service
@RequiredArgsConstructor
public class AiIntegrationService {

    private final DtcRepository dtcRepository;
    private final CarMakeRepository carMakeRepository;
    private final CarModelRepository carModelRepository;
    private final CarTrimRepository carTrimRepository;
    private final RepairRepository repairRepository;
    private final PartRepository partRepository;
    private final ToolRepository toolRepository;

    public AiContextResponse getContext(String code, String make, String model, String trim, Integer year) {
        String dtcDescription = dtcRepository.findByCodeIgnoreCase(code)
                .map(DtcCode::getDescription)
                .orElse(null);

        List<RepairProcedureResponse> existing = repairRepository.findByDtcCodeIgnoreCase(code).stream()
                .map(this::toResponse)
                .toList();

        return AiContextResponse.builder()
                .code(code)
                .dtcDescription(dtcDescription)
                .make(make)
                .model(model)
                .trim(trim)
                .year(year)
                .existingProcedures(existing)
                .build();
    }

    public RepairProcedureResponse saveRepairProcedure(RepairProcedureRequest request) {
        List<Part> parts = request.parts() == null ? List.of()
                : request.parts().stream()
                        .map(this::findOrCreatePart)
                        .toList();
        List<Tool> tools = request.tools() == null ? List.of()
                : request.tools().stream()
                        .map(this::findOrCreateTool)
                        .toList();

        RepairProcedure saved = repairRepository.save(RepairProcedure.builder()
                .dtcCode(request.dtcCode())
                .vehicleMake(request.vehicleMake())
                .vehicleModel(request.vehicleModel())
                .vehicleTrim(request.vehicleTrim())
                .vehicleYear(request.vehicleYear())
                .title(request.title())
                .steps(request.steps())
                .parts(parts)
                .tools(tools)
                .build());

        return toResponse(saved);
    }

    private Part findOrCreatePart(PartRequest request) {
        return partRepository.findByNameIgnoreCase(request.name())
                .orElseGet(() -> partRepository.save(Part.builder()
                        .name(request.name())
                        .partNumber(request.partNumber())
                        .estimatedPrice(request.estimatedPrice())
                        .build()));
    }

    private Tool findOrCreateTool(ToolRequest request) {
        return toolRepository.findByNameIgnoreCase(request.name())
                .orElseGet(() -> toolRepository.save(Tool.builder().name(request.name()).build()));
    }

    private RepairProcedureResponse toResponse(RepairProcedure p) {
        return RepairProcedureResponse.builder()
                .id(p.getId())
                .dtcCode(p.getDtcCode())
                .vehicleMake(p.getVehicleMake())
                .vehicleModel(p.getVehicleModel())
                .vehicleTrim(p.getVehicleTrim())
                .vehicleYear(p.getVehicleYear())
                .title(p.getTitle())
                .steps(p.getSteps())
                .parts(Optional.ofNullable(p.getParts()).orElse(List.of()).stream().map(Part::getName).toList())
                .tools(Optional.ofNullable(p.getTools()).orElse(List.of()).stream().map(Tool::getName).toList())
                .build();
    }
}
