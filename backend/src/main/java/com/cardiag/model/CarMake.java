package com.cardiag.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import lombok.*;

/**
 * Reference make data fetched from CarAPI (external "id" used as primary key).
 */
@Entity
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CarMake {

    @Id
    private Long id;

    private String name;
}
