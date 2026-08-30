package com.cardiag.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import lombok.*;

/**
 * Reference trim data fetched from CarAPI (external "id" used as primary key).
 */
@Entity
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CarTrim {

    @Id
    private Long id;

    private String name;
    private Long modelId;
    private String makeName;
    private String modelName;
    private Integer year;
}
