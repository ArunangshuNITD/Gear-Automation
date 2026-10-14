import tkinter as tk
from pathlib import Path

from calculations.gear_calculation import calculate_gear_design
from profiles.involute_profile import generate_involute_profile, generate_profile_report


RESULTS_DIR = Path(__file__).resolve().parent / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

root = tk.Tk()
root.withdraw()


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

    tk.Button(btn_frame, text="Close", command=save_and_close, width=12, bg="#238636", fg="white").pack(side="left", padx=5)
    window.protocol("WM_DELETE_WINDOW", save_and_close)


def show_profile_report():
    open_report_window(
        "Gear Profile Calculation Report",
        profile["report"],
        next_callback=show_profile_plot,
    )


def show_profile_plot():
    root.destroy()
    generate_involute_profile(m=design["m"], z=design["z"], pressure_angle=design["pressure_angle"])


design = calculate_gear_design()
profile = generate_profile_report(design["m"], design["z"], design["pressure_angle"])

open_report_window(
    "Gear Design Report",
    design["report"],
    next_callback=show_profile_report,
)

root.mainloop()
