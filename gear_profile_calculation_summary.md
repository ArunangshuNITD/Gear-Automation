# Gear Profile Calculation Summary

This summary explains the logic in the profiling scripts (like `involute_profile.py` and `extract_3d_profile.py`) and how the continuous involute gear profile is generated for both 2D plotting and 3D CAD modeling.

## 1. Purpose of the script

The script creates a simplified involute gear profile from three main inputs:

- `m` = module (mm)
- `z` = number of teeth
- `pressure_angle` = pressure angle in degrees

It calculates the gear geometry, generates the involute curve for each tooth, and exports a continuous mathematical boundary used for visualization or 3D extrusion.

---

## 2. Inputs and meaning

The program starts with baseline parameters, for example:

```python
m = 12
z = 18
pressure_angle = 20
```

These values define a gear size and tooth geometry.

The key idea is:

- the pitch circle is the reference circle used for gear meshing
- the involute profile is created from the base circle
- the pressure angle controls how the teeth lean and mesh

---

## 3. Core gear geometry formulas

### Pitch circle radius

```python
r_p = m * z / 2
```

This is the radius of the pitch circle.

### Pressure angle in radians

```python
phi = np.radians(pressure_angle)
```

The script converts the pressure angle from degrees to radians because Python math functions expect radians.

### Base circle radius

```python
r_b = r_p * math.cos(phi)
```

The base circle is important because the involute is generated from it. The involute is the path traced by a point on a taut string unwinding from the base circle.

### Addendum circle radius

```python
r_a = r_p + m
```

This is the outside radius of the gear tooth.

### Root circle radius

```python
r_r = r_p - (1.25 * m)
```

This is the lower limit of the tooth profile, near the root.

---

## 4. Derived dimensions in the report

The script also computes and prints:

```python
pitch diameter = 2 * r_p
base diameter = 2 * r_b
addendum diameter = 2 * r_a
root diameter = 2 * r_r
```

It also calculates:

```python
circular pitch = π * m
tooth thickness at pitch = π * m / 2
```

These values help describe the spacing and tooth width of the gear.

---

## 5. Involute mathematics

The involute curve is parameterized by a variable `t`.

The script uses:

```python
t_max = math.sqrt((r_a / r_b) ** 2 - 1)
t = np.linspace(0, t_max, 100)
```

This sets the valid range of the involute from the base circle up to the outer tooth tip.

The involute coordinates are generated using:

```python
x_inv = r_b * (np.cos(t) + (t * np.sin(t)))
y_inv = r_b * (np.sin(t) - (t * np.cos(t)))
```

This is the standard involute-of-a-circle equation.

Where:

- `x_inv` and `y_inv` are the coordinates of the involute curve
- `r_b` is the base circle radius
- `t` is the involute parameter

This is the curve that forms the tooth flank.

---

## 6. Tooth offset and rotation (Continuous 3D Logic)

For gear teeth, the involute profile must be rotated into the correct position. 

The script computes:
```python
inv_phi = np.tan(phi) - phi
offset = (np.pi / (2 * z)) - inv_phi
```
This offset helps center the angular positions. However, a key geometric quirk is that the base rotation actually targets the **center of the root gap**, not the center of the tooth!

Therefore, to build a solid gear tooth continuously, we must pair the right flank of the current gap (index `i`) with the left flank of the **next** gap (index `i + 1`):
```python
teeth_angle = i * 2 * np.pi / z
next_teeth_angle = ((i + 1) % z) * 2 * np.pi / z

angle_right = teeth_angle + offset
angle_next_left = next_teeth_angle - offset
```
By doing this, the right side and left side point outward to form a solid tooth structure, rather than inward to form an hourglass shape.

---

## 7. Flow of the continuous extraction logic

To create a closed 3D spline for CAD software (like SolidWorks), the points must be drawn sequentially in a continuous, unbroken loop. The program uses the following sequence inside the `for i in range(z):` loop:

### Step 1: Calculate Flanks and Roots
The script computes the coordinates for the current right flank (`x_right`, `y_right`) and the next left flank (`x_next_left`, `y_next_left`). It also calculates the exact angular positions of where these flanks intersect the root circle (`x_root_right`, `y_root_right`, etc.).

### Step 2: Walk UP the Right Flank
The script generates a straight line from the root circle up to the base circle, and appends those points. Then, it appends the involute points for the right flank, traveling UP to the tip of the tooth.

### Step 3: Draw ACROSS the Tip
Instead of just two points, the script generates a uniform array of points across the top of the tooth:
```python
tip_x = np.linspace(x_right[-1], x_next_left[-1], 10)
```
This ensures high-quality CAD extrusion without visual gaps.

### Step 4: Walk DOWN the Left Flank
To maintain a continuous loop, the array for the left flank is reversed `[::-1]` so the path travels DOWN from the tip to the base circle, followed by a straight line DOWN to the root circle.

### Step 5: Draw the Root Arc to the Next Tooth
Finally, to connect the current tooth to the start of the next tooth, the script generates an arc along the root circle:
```python
root_arc_angles = np.linspace(theta_next_left, theta_next_right, 10)
```
This closes the gap, and the loop repeats, resulting in a single, continuous list of `(x, y, z)` coordinates representing the perfect gear boundary.

---

## 8. Important geometric meaning

This script captures the essential gear tooth geometry required for both analytical modeling and physical manufacturing representations:

- pitch circle = center reference for gear mesh
- base circle = source of the involute curve
- addendum = tooth tip
- root = lower tooth region
- involute curve = tooth flank profile

The key engineering idea is that each tooth flank is generated as an involute of the base circle, which gives smooth meshing between gears.

---

## 9. Simple visual interpretation

Imagine a string unwinding from a base circle. The end of the string traces an involute curve.

That involute is used as the tooth flank because it provides:

- smooth contact between gear teeth
- consistent motion transfer
- good meshing behavior under pressure angle design

---

## 10. Summary in one sentence

This script takes module, number of teeth, and pressure angle, computes the fundamental gear geometry, generates involute flanks, and mathematically chains them together into a continuous, ordered perimeter ready for 2D visualization and 3D CAD modeling.