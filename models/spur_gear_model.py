import csv
import win32com.client
from pathlib import Path

def draw_gear_in_solidworks(csv_filename):
    print("Reading points from CSV...")
    points = []
    
    # Read the extracted points
    with open(csv_filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            # Convert string coordinates back to floats
            points.append((float(row[0]), float(row[1]), float(row[2])))

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

    # Select the Front Plane and open a sketch
    # Using the simpler SelectByID method avoids the Callout pointer Type Mismatch
    swModel.SelectByID("Front Plane", "PLANE", 0.0, 0.0, 0.0)
    swModel.SketchManager.InsertSketch(True)
    
    # Disable screen updating for faster drawing
    swModel.SketchManager.AddToDB = True
    
    print("Drawing sketch lines... this may take a few seconds.")
    
    # Loop through the points to draw continuous lines
    for i in range(len(points) - 1):
        x1, y1, z1 = points[i]
        x2, y2, z2 = points[i + 1]
        
        # Divide by 1000 to convert mm to meters for the SW API
        swModel.SketchManager.CreateLine(
            x1 / 1000.0, y1 / 1000.0, 0, 
            x2 / 1000.0, y2 / 1000.0, 0
        )
        
    # Re-enable screen updating
    swModel.SketchManager.AddToDB = False
    
    # Clear the selection and rebuild to finalize the sketch
    swModel.ClearSelection2(True)
    swModel.EditRebuild3()
    
    print("Sketch generation complete! You can now extrude the gear in SolidWorks.")

if __name__ == "__main__":
    # Point this to the CSV generated in your results folder
# Add one more .parent to go up to the main project directory
    csv_path = Path(__file__).resolve().parent.parent / "results" / "gear_3d_profile_points.csv"
    if csv_path.exists():
        draw_gear_in_solidworks(csv_path)
    else:
        print("CSV not found. Please run main.py to generate the points first.")