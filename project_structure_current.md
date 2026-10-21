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
│   └── gear_mesh_validation_report.txt (generated when workflow runs)
├── gear_gui.py
├── main.py
├── profile_calculation_summary.md
├── project_structure_current.md
├── workflow.md
├── target.txt
├── __pycache__/
└── README.md (optional, if added later)
```

## Folder descriptions

- `calculations/` — contains the gear design calculation logic, selected module sizing, and design report generation.
- `profiles/` — contains gear geometry plotting, involute profile generation, and paired gear visualization.
- `validation/` — contains the mesh validation logic used to confirm pitch diameters and transmission ratio before generating the profile.
- `figures/` — stores generated images such as the profile plot and pair visualization.
- `results/` — stores text exports of design reports, profile reports, and validation reports.
- `gear_gui.py` — Tkinter GUI entry point for showing reports in sequence.
- `main.py` — main workflow runner that performs the design calculation, mesh validation, and profile generation steps.
- `profile_calculation_summary.md` — summary of the involute profile geometry and plotting logic.
- `project_structure_current.md` — current project documentation.
- `workflow.md` — explains the required order of operations in the design workflow.
- `target.txt` — project specification and reference notes.
- `__pycache__/` — Python-generated cache files.

## Current workflow

The program now follows this sequence:

1. `calculate_gear_design()` computes the selected module, tooth count, diameters, and design report.
2. The design result is normalized and passed to `validate_gear_mesh()`.
3. If validation fails, the mesh validation report is shown and the workflow stops before profile generation.
4. If validation passes, the gear profile report is created.
5. The GUI opens the design report and then the validation report, followed by the profile report.
6. `generate_involute_profile()` creates the final gear plot and saves it in `figures/gear_profile.png`.

## Notes

- The project contains both the analytical design stage and the geometric validation stage.
- Validation is now intentionally placed before the profile calculation so invalid gear meshes are rejected early.
- This layout is suitable for a small gear automation prototype and can be extended with more analysis, tests, and UI controls.
