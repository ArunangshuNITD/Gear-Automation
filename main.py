import csv
from pathlib import Path
import runpy
import tkinter as tk

from calculations.gear_calculation import calculate_gear_design
from models.spur_gear_model import draw_gear_in_solidworks
from profiles.extract_3d_profile import get_continuous_gear_profile
from profiles.involute_profile import generate_involute_profile, generate_profile_report
from validation.gear_mesh_validation import build_mesh_validation_report, validate_gear_mesh

PROJECT_ROOT = Path(__file__).resolve().parent
RESULTS_DIR = PROJECT_ROOT / "results"
MODELS_DIR = PROJECT_ROOT / "models"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

root = tk.Tk()
root.withdraw()

design = {}
profile = {}
mesh_report = ""


def save_report_to_file(title_text, report_text):
    file_name = "gear_calculation_report.txt" if "DESIGN" in title_text.upper() else "gear_profile_calculation_report.txt"
    path = RESULTS_DIR / file_name
    path.write_text(report_text, encoding="utf-8")
    return path


def open_report_window(title_text, report_text, next_callback=None):
    window = tk.Toplevel(root)
    window.title(title_text)
    window.geometry("900x600")

    text_widget = tk.Text(
        window,
        wrap="none",
        font=("Consolas", 10),
        bg="#0d1117",
        fg="#c9d1d9",
        padx=12,
        pady=12,
    )
    text_widget.insert("end", report_text)
    text_widget.configure(state="disabled")
    text_widget.pack(fill="both", expand=True, padx=10, pady=(10, 5))

    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=(0, 10))

    def save_and_close():
        save_report_to_file(title_text, report_text)
        window.destroy()
        if next_callback:
            next_callback()

    tk.Button(
        btn_frame,
        text="Close",
        command=save_and_close,
        width=12,
        bg="#238636",
        fg="white",
    ).pack(side="left", padx=5)

    window.protocol("WM_DELETE_WINDOW", save_and_close)


def show_mesh_validation_report():
    if not mesh_report:
        return
    open_report_window(
        "Gear Mesh Validation Report",
        mesh_report,
        next_callback=show_profile_report,
    )


def show_profile_report():
    open_report_window(
        "Gear Profile Calculation Report",
        profile.get("report", ""),
        next_callback=show_profile_plot,
    )


def show_profile_plot():
    # Close GUI cleanly so it doesn't freeze during CAD processing
    root.destroy()

    # 1. Generate 2D Profile Plot
    generate_involute_profile(
        m=design["m"],
        z=design["z"],
        pressure_angle=design["pressure_angle"],
    )

    # 2. Extract 3D Continuous Coordinates & Save CSV
    points = get_continuous_gear_profile(
        m=design["m"],
        z=design["z"],
        pressure_angle=design["pressure_angle"],
    )
    csv_path = RESULTS_DIR / "gear_3d_profile_points.csv"

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["X (mm)", "Y (mm)", "Z (mm)"])
        writer.writerows(points)
    print(f"Saved {len(points)} continuous 3D points to: {csv_path}")

    # 3. Model in SolidWorks & Save to models/
    profile_part = MODELS_DIR / "spur_gear_profile.sldprt"
    solid_part = MODELS_DIR / "spur_gear_3d.sldprt"
    face_width_mm = float(design.get("b", 30.0))

    print(f"Generating SolidWorks profile + 3D solid: {profile_part} -> {solid_part}")
    draw_gear_in_solidworks(
        csv_path,
        profile_output_path=profile_part,
        solid_output_path=solid_part,
        face_width=face_width_mm,
    )


def main():
    global design, profile, mesh_report

    design = calculate_gear_design()

    # Backfill required gear mesh validation parameters
    design["Z_p"] = design.get("Z_p", design.get("z"))
    design["Z_g"] = design.get("Z_g", int(design["Z_p"] * design["i"]))
    design["D_p"] = design.get("D_p", design["m"] * design["Z_p"])
    design["D_g"] = design.get("D_g", design["m"] * design["Z_g"])

    mesh_checks = validate_gear_mesh(design)
    mesh_report = build_mesh_validation_report(design, mesh_checks)

    if not mesh_checks.get("overall_pass", False):
        print("Gear mesh validation failed. Stopping before profile generation.")
        open_report_window("Gear Mesh Validation Report", mesh_report, next_callback=root.quit)
        root.mainloop()
        return

    profile = generate_profile_report(design["m"], design["z"], design["pressure_angle"])

    open_report_window(
        "Gear Design Report",
        design["report"],
        next_callback=show_mesh_validation_report,
    )

    root.mainloop()


if __name__ == "__main__":
    main()

    # Optional: Execute pair visualization script afterward
    gear_pair_path = PROJECT_ROOT / "profiles" / "gear_pair.py"
    if gear_pair_path.exists():
        try:
            runpy.run_path(str(gear_pair_path), run_name="__main__")
        except Exception as exc:
            print("Failed to run profiles/gear_pair.py:", exc)
    else:
        print("profiles/gear_pair.py not found at:", gear_pair_path)