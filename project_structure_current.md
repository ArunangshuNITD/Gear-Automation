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
│   └── involute_profile.py
├── results/
│   ├── gear_calculation_report.txt
│   └── gear_profile_calculation_report.txt
├── gear_gui.py
├── main.py
├── project_structure_current.md
├── target.txt
├── venv/
├── __pycache__/
└── README.md (optional, if added later)
```

## Folder descriptions

- `calculations/` — contains the gear design calculation logic and report generation.
- `figures/` — stores generated gear profile images.
- `profiles/` — contains the involute gear geometry and plotting logic.
- `results/` — stores generated calculation reports and export files.
- `gear_gui.py` — Tkinter-based GUI for showing the calculation and profile reports in sequence.
- `main.py` — entry point for the full workflow: calculate design, save reports, and generate the gear profile.
- `venv/` — Python virtual environment used for project dependencies.
- `project_structure_current.md` — documentation of the current structure.
- `target.txt` — reference file describing the project intent and target architecture.
- `__pycache__/` — Python cache generated during execution.

## Notes

- The project now includes both the calculation workflow and the profile generation workflow.
- The report generation and gear profile generation are connected through the selected module, tooth count, and pressure angle.
- The structure is suitable for a small gear design automation prototype and can be extended with tests, validation, and UI refinements later.
