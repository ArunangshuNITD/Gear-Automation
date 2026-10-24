# Gear Design Workflow

This document describes the current operational flow of the gear design automation project as implemented in the codebase.

## 1. Main execution path

The application begins in `main.py` and follows this sequence:

1. `calculate_gear_design()` from `calculations/gear_calculation.py`
2. Mesh validation via `validate_gear_mesh()` in `validation/gear_mesh_validation.py`
3. Profile report generation via `generate_profile_report()` in `profiles/involute_profile.py`
4. Involute plot generation via `generate_involute_profile()`
5. Optional paired-gear plot execution from `profiles/gear_pair.py`

---

## 2. Design calculation stage

The first stage is handled by:

- `calculations/gear_calculation.py`
- `calculate_gear_design()`

This function computes the design data for a spur gear pair, including:

- module `m`
- pinion teeth `Z_p`
- gear teeth `Z_g`
- pitch diameters `D_p`, `D_g`
- ratio `i`
- design report text
- selected standard module and safety checks

The function returns a dictionary with the computed values and a formatted report string.

---

## 3. Validation stage

The next stage is handled by:

- `validation/gear_mesh_validation.py`
- `validate_gear_mesh(d)`
- `build_mesh_validation_report(d, checks)`

The project currently validates the mesh using these required fields:

- `m`
- `Z_p`
- `Z_g`
- `D_p`
- `D_g`
- `i`

The checks performed are:

- pinion pitch diameter: `abs(m * Z_p - D_p) < 1e-6`
- gear pitch diameter: `abs(m * Z_g - D_g) < 1e-6`
- transmission ratio: `abs(i - (Z_g / Z_p)) < 1e-6`

If any required field is missing or any check fails, the workflow stops before profile generation and opens the validation report.

---

## 4. Profile report stage

If validation passes, the workflow creates a profile report using:

- `profiles/involute_profile.py`
- `generate_profile_report(m, z, pressure_angle)`

This report contains:

- pitch circle radius
- base circle radius
- addendum radius
- root radius
- pitch diameter
- base diameter
- circular pitch
- tooth thickness at pitch

---

## 5. Plot generation stage

After the profile report is created, the program calls:

- `generate_involute_profile(m, z, pressure_angle)`

This function draws the involute tooth geometry and saves the output to:

- `figures/gear_profile.png`

The script also runs `profiles/gear_pair.py` after the GUI workflow so the pair visualization can be generated as a follow-up step.

---

## 6. GUI flow

The GUI sequence is:

1. Design report
2. Mesh validation report
3. Profile report
4. Profile plot

This behavior is implemented in `main.py` with `open_report_window()` and the callback chain.

---

## 7. Stop condition

If `validate_gear_mesh()` returns `overall_pass == False`, the program is designed to stop before creating the gear profile calculations and plots.

This prevents invalid gear geometry from being visualized or exported.

---

## 8. Current design baseline

The current project is using:

- module: `12 mm`
- pinion teeth: `18`
- gear teeth: `72`
- gear ratio: `4:1`
- pressure angle: `20 deg`

The corresponding mesh is validated as:

- `D_p = m * Z_p = 216 mm`
- `D_g = m * Z_g = 864 mm`
- `i = Z_g / Z_p = 4`

This is the baseline used by the current automated workflow.
