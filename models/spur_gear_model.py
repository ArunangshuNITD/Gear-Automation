import csv
from pathlib import Path
import win32com.client


def draw_gear_in_solidworks(csv_filename, profile_output_path=None, solid_output_path=None, face_width=30.0):
    print("Reading points from CSV...")
    points = []

    with open(csv_filename, 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header
        for row in reader:
            if not row:
                continue
            points.append((float(row[0]), float(row[1]), float(row[2])))

    if not points:
        print("No points found in CSV file.")
        return

    # Determine default paths if not explicitly passed
    # models/ folder is the parent of this file
    models_dir = Path(__file__).resolve().parent
    if profile_output_path is None:
        profile_output_path = models_dir / "spur_gear_profile.sldprt"
    if solid_output_path is None:
        solid_output_path = models_dir / "spur_gear_3d.sldprt"

    profile_output_path.parent.mkdir(parents=True, exist_ok=True)
    solid_output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Loaded {len(points)} points. Connecting to SolidWorks...")

    try:
        swApp = win32com.client.Dispatch("SldWorks.Application")
        swApp.Visible = True
    except Exception:
        print("Failed to connect. Is SolidWorks open?")
        return

    swModel = swApp.ActiveDoc
    if swModel is None:
        print("Error: Please open a blank part document in SolidWorks first!")
        return

    # Select Front Plane and start sketch
    swModel.SelectByID("Front Plane", "PLANE", 0.0, 0.0, 0.0)
    swModel.SketchManager.InsertSketch(True)
    swModel.SketchManager.AddToDB = True

    print("Drawing sketch lines... this may take a few seconds.")
    for i in range(len(points) - 1):
        x1, y1, _ = points[i]
        x2, y2, _ = points[i + 1]
        swModel.SketchManager.CreateLine(
            x1 / 1000.0, y1 / 1000.0, 0.0,
            x2 / 1000.0, y2 / 1000.0, 0.0
        )

    swModel.SketchManager.AddToDB = False
    
    # Close sketch and get its feature
    swModel.SketchManager.InsertSketch(True)
    swModel.ClearSelection2(True)

    # Save the 2D sketched profile
    if profile_output_path is not None:
        print(f"Saving sketched profile to: {profile_output_path}")
        swModel.SaveAs3(str(profile_output_path), 0, 1)

    print("Extruding gear body...")
    depth_meters = float(face_width) / 1000.0

    # Select the profile sketch (tries Sketch1; if renamed/localized, selects the latest sketch)
    selected = swModel.SelectByID("Sketch1", "SKETCH", 0.0, 0.0, 0.0)
    if not selected:
        # Fallback: select last active feature
        swModel.Extension.SelectByID2("", "SKETCH", 0.0, 0.0, 0.0, False, 0, None, 0)

    swModel.FeatureManager.FeatureExtrusion3(
        True,               # Sd (Single-ended)
        False,              # Flip direction
        False,              # Dir
        0,                  # T1 (0 = Blind)
        0,                  # T2
        depth_meters,       # Depth 1 (meters)
        0.0,                # Depth 2
        False, False,       # Draft
        False, False,
        0.0, 0.0,           # Draft angles
        False, False, False, False,
        True, True, True,   # Merge, UseFeatScope, UseAutoSelect
        0, 0, False
    )

    swModel.ClearSelection2(True)

    # Save the extruded 3D solid part
    print(f"Saving extruded 3D solid to: {solid_output_path}")
    swModel.SaveAs3(str(solid_output_path), 0, 1)
    print("Part saved successfully!")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "results" / "gear_3d_profile_points.csv"
    profile_path = project_root / "models" / "spur_gear_profile.sldprt"
    solid_path = project_root / "models" / "spur_gear_3d.sldprt"

    if csv_path.exists():
        draw_gear_in_solidworks(csv_path, profile_path, solid_path, face_width=30.0)
    else:
        print(f"CSV not found at: {csv_path}. Please run main.py first.")