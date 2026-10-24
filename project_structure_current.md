# Gear Design Automation

## Current project structure

```text
Gear Design Automation/
├── calculations/
│   ├── __pycache__/
│   └── gear_calculation.py
├── figures/
│   └── gear_profile.png
├── profiles/
│   ├── __pycache__/
│   ├── gear_pair.py
│   └── involute_profile.py
├── validation/
│   ├── __pycache__/
│   └── gear_mesh_validation.py
├── results/
│   ├── gear_calculation_report.txt
│   ├── gear_profile_calculation_report.txt
│   └── gear_mesh_validation_report.txt  (generated during validation)
├── gear_gui.py
├── main.py
├── profile_calculation_summary.md
├── project_structure_current.md
├── workflow.md
├── target.txt
├── __pycache__/
└── README.md  (optional, if added later)
```

## Folder descriptions

- `calculations/` — contains the spur gear design calculation logic and design report generation.
- `profiles/` — contains the involute profile generation, plot logic, and pair-gear visualization.
- `validation/` — contains the mesh validation logic used before profile generation.
- `figures/` — stores generated profile images.
- `results/` — stores text report exports for the design and profile process.
- `gear_gui.py` — GUI entry point for showing report windows in sequence.
- `main.py` — main workflow runner that calculates, validates, and reports the design.
- `profile_calculation_summary.md` — summary of the involute profile mathematics and plotting logic.
- `project_structure_current.md` — current project document.
- `workflow.md` — execution workflow description.
- `target.txt` — current design goals and implementation target.
- `__pycache__/` — Python cache files.

## Current workflow

The program currently follows this sequence:

1. `calculate_gear_design()` computes the selected module, tooth counts, diameters, and design report.
2. `design` data is normalized and passed to `validate_gear_mesh()`.
3. If the validation fails, the mesh validation report is shown and the workflow stops.
4. If validation passes, the profile report is generated from `generate_profile_report()`.
5. The GUI opens the design report and then the mesh validation report, followed by the profile report.
6. `generate_involute_profile()` creates the final gear plot and saves `figures/gear_profile.png`.
7. `profiles/gear_pair.py` may execute afterward to generate the paired gear visualization.

## Notes

- The project includes both the analytical calculation stage and the geometric validation stage.
- Validation is intentionally placed before profile generation so invalid gear meshes are rejected early.
- The current layout is suitable for a small gear automation prototype and can be expanded with more analysis or UI controls.
