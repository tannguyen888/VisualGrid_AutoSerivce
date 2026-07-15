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
public class Assembly {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String code;
    private String name;

    @ManyToMany
    @JoinTable(
            name = "assembly_component",
            joinColumns = @JoinColumn(name = "assembly_id"),
            inverseJoinColumns = @JoinColumn(name = "component_id")
    )
    private List<Component> components;
}
