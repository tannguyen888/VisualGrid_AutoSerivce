package com.cardiag.model;

import jakarta.persistence.*;
import lombok.*;

/** A tool needed to carry out a repair procedure. */
@Entity
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Tool {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true)
    private String name;
}
