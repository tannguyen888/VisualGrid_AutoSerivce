package com.cardiag.model;

import jakarta.persistence.*;
import lombok.*;

import java.util.List;

@Entity
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RepairProcedure {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;

    @Column(columnDefinition = "TEXT")
    private String steps;

    /** OBD/DTC code this procedure addresses, e.g. P0301. */
    private String dtcCode;

    private String vehicleMake;
    private String vehicleModel;
    private String vehicleTrim;
    private Integer vehicleYear;

    @ManyToMany
    @JoinTable(name = "repair_procedure_part", joinColumns = @JoinColumn(name = "repair_procedure_id"), inverseJoinColumns = @JoinColumn(name = "part_id"))
    private List<Part> parts;

    @ManyToMany
    @JoinTable(name = "repair_procedure_tool", joinColumns = @JoinColumn(name = "repair_procedure_id"), inverseJoinColumns = @JoinColumn(name = "tool_id"))
    private List<Tool> tools;
}
