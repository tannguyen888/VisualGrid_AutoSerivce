package com.cardiag.model;

import jakarta.persistence.*;
import lombok.*;

/** A physical part that may be needed to complete a repair procedure. */
@Entity
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Part {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true)
    private String name;

    private String partNumber;
    private Double estimatedPrice;
}
