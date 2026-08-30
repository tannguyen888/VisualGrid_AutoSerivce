package com.cardiag.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import lombok.*;

/**
 * Reference model data fetched from CarAPI (external "id" used as primary key).
 */
@Entity
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CarModel {

    @Id
    private Long id;

    private String name;
    private Long makeId;
    private String makeName;
    private Integer year;
}
