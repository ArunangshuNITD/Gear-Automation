# Gear Design Workflow

This document explains the operational flow of the gear design automation project.

## 1. Main sequence

The application is intended to run in this order:

1. Calculate the gear design
2. Validate the gear mesh geometry
3. Generate the gear profile report
4. Plot the involute gear profile

---

## 2. Step 1 — Gear design calculation

The first stage is handled by:

- `calculations/gear_calculation.py`
- `calculate_gear_design()`

This function computes:

- module `m`
- pinion tooth count `Z_p`
- gear tooth count `Z_g`
- pitch diameters `D_p`, `D_g`
- speed ratio `i`
- design report text

The result is returned as a dictionary containing the design values and a human-readable report.

---

## 3. Step 2 — Gear mesh validation

The next stage is handled by:

- `validation/gear_mesh_validation.py`
- `validate_gear_mesh(d)`
- `build_mesh_validation_report(d, checks)`

This validation checks whether the gear geometry is internally consistent before profile generation begins.

The required keys are:

- `m`
- `Z_p`
- `Z_g`
- `D_p`
- `D_g`
- `i`

The validation checks are:

- pinion pitch diameter: `m * Z_p == D_p`
- gear pitch diameter: `m * Z_g == D_g`
- transmission ratio: `i == Z_g / Z_p`

If any required value is missing or the checks fail, the workflow should stop and show the mesh validation report.

---

## 4. Step 3 — Profile calculation report

If validation passes, the next step is:

- `profiles/involute_profile.py`
- `generate_profile_report(m, z, pressure_angle)`

This builds a text report containing the gear profile data such as:

- pitch circle radius
- base circle radius
- addendum radius
- root radius
- pitch diameter
- base diameter

This report is then shown in the Tkinter window.

---

## 5. Step 4 — Gear profile plot

After the profile report, the program calls:

- `generate_involute_profile(m, z, pressure_angle)`

This function draws the tooth geometry as an involute profile and saves the output image to:

- `figures/gear_profile.png`

---

## 6. GUI flow

The GUI sequence is expected to be:

1. Design report
2. Mesh validation report
3. Profile report
4. Profile plot

This is handled in the main application flow and reflected in the current report windows.

---

## 7. Stop condition

If the mesh validation returns `overall_pass == False`, the application is designed to stop before the gear profile calculation and plot are created. This prevents invalid gear geometry from being visualized.

---

## 8. Example of the logic

```python
design = calculate_gear_design()

design["Z_p"] = design.get("Z_p", design.get("z"))
design["Z_g"] = design.get("Z_g", int(design["Z_p"] * design["i"]))
design["D_p"] = design.get("D_p", design["m"] * design["Z_p"])
design["D_g"] = design.get("D_g", design["m"] * design["Z_g"])

mesh_checks = validate_gear_mesh(design)
if not mesh_checks.get("overall_pass", False):
    show_mesh_validation_report()
    return

profile = generate_profile_report(design["m"], design["z"], design["pressure_angle"])
generate_involute_profile(design["m"], design["z"], design["pressure_angle"])
```

This is the intended control flow for the automation process.
