from pathlib import Path

from calculations.gear_calculation import calculate_gear_design
from profiles.involute_profile import (
    generate_involute_profile,
    generate_profile_report,
)


def main():
    design = calculate_gear_design()
    results_dir = Path(__file__).resolve().parent / "results"
    results_dir.mkdir(exist_ok=True)

    report_path = results_dir / "gear_calculation_report.txt"
    report_path.write_text(design["report"], encoding="utf-8")

    m = design["m"]
    z = design["z"]
    pressure_angle = design["pressure_angle"]

    if m is None:
        raise ValueError("No valid gear module was selected from the design check.")

    print("\n=== GEAR DESIGN REPORT ===")
    print(design["report"])

    profile_report = generate_profile_report(m, z, pressure_angle)
    profile_path = results_dir / "gear_profile_calculation_report.txt"
    profile_path.write_text(profile_report["report"], encoding="utf-8")

    print("\n=== PROFILE CALCULATION REPORT ===")
    print(profile_report["report"])

    generate_involute_profile(m=m, z=z, pressure_angle=pressure_angle)


if __name__ == "__main__":
    main()
