# Rotating Blade Stress Field Simulation

## Overview
This repository contains a Python-based **modeling and simulation project** developed for  
**ME 150: Modeling and Simulation of Advanced Manufacturing Processes**.

The project models internal force resultants and **deviatoric stress fields in a rotating blade**
subjected to centrifugal and tangential inertial effects. The objective is to demonstrate
physics-based modeling, analytical derivation of governing relations, and numerical post-processing
of stress fields under increasing rotational loads.

---

## Modeling Framework

The blade is modeled using beam theory with distributed inertial loading:

- Rectangular cross-section
- Free-end boundary conditions at the blade tip
- Distributed body forces induced by rotation and angular acceleration

Internal resultants are derived analytically:
- **Axial force** from centrifugal effects
- **Shear force** from angular acceleration
- **Bending moment** from centrifugal loading

These resultants are mapped onto the blade cross-section to compute:
- Normal stress from axial force and bending
- Shear stress using a rectangular-section shear formulation

A **deviatoric stress norm** is evaluated under plane stress assumptions and visualized using
contour plots.

---

## Assumptions

- Linear elastic material behavior  
- Small deformations  
- Beam theory applicable along the blade span  
- Plane stress approximation across the cross-section  
- Inertial loading dominates (no aerodynamic or thermal effects)  

---

## Numerical Implementation

- **Language:** Python  
- **Libraries:** NumPy, Matplotlib  
- **Discretization:**
  - Spanwise discretization along the blade length
  - Cross-sectional discretization across the blade width  

For each operating condition `(ω, α)`, the simulation:
1. Computes distributed inertial loads
2. Evaluates internal force resultants
3. Computes stress components
4. Visualizes the deviatoric stress norm

All figures are generated automatically and saved to disk.

---

## Operating Conditions

The blade response is evaluated for multiple rotational states defined by paired values of:
- Angular velocity `ω`
- Angular acceleration `α`

Each state produces a corresponding stress contour plot.

---

## Output

- 2D contour plots of the **deviatoric stress norm**
- One plot per operating condition
- Figures saved to an output directory for post-processing and reporting

---

## Academic Context

This project was completed for  
**ME 150: Modeling and Simulation of Advanced Manufacturing Processes**.

The modeling approach, governing equations, and stress formulations are informed by material
presented in **T. I. Zohdi’s course reader**, which emphasizes physics-based modeling,
reduced-order representations, and computational analysis of advanced manufacturing systems.

All code implementation, numerical setup, and visualization were completed by the author.

---

## Reference

Zohdi, T. I.  
*Lecture Notes: Modeling and Simulation Tools for Industrial Research Applications –  
Fundamentals and Advanced Manufacturing*  
University of California, Berkeley.

---

## Notes

This model is intended for:
- Educational modeling and simulation
- Conceptual stress analysis of rotating structures
- Demonstration of analytical–numerical coupling

It is not intended to replace high-fidelity finite element analysis.

---

## Author
Oscar Lopez
