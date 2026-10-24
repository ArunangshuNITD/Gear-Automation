import math
import numpy as np
import matplotlib.pyplot as plt

def get_continuous_gear_profile(m, z, pressure_angle):
    r_p = m * z / 2
    phi = np.radians(pressure_angle)
    r_b = r_p * math.cos(phi)
    r_a = r_p + m
    r_r = r_p - (1.25 * m)
    
    t_max = math.sqrt((r_a / r_b)**2 - 1)
    t = np.linspace(0, t_max, 100)
    
    x_inv = r_b * (np.cos(t) + (t * np.sin(t)))
    y_inv = r_b * (np.sin(t) - (t * np.cos(t)))
    
    inv_phi = np.tan(phi) - phi
    offset = (np.pi / (2 * z)) - inv_phi
    
    continuous_points = []
    
    for i in range(z):
        teeth_angle = i * 2 * np.pi / z
        next_teeth_angle = ((i + 1) % z) * 2 * np.pi / z
        
        angle_right = teeth_angle + offset
        angle_next_left = next_teeth_angle - offset
        
        x_right = (x_inv * np.cos(angle_right)) - (y_inv * np.sin(angle_right))
        y_right = (x_inv * np.sin(angle_right)) + (y_inv * np.cos(angle_right))
        
        x_next_left = (x_inv * np.cos(angle_next_left)) + (y_inv * np.sin(angle_next_left))
        y_next_left = (x_inv * np.sin(angle_next_left)) - (y_inv * np.cos(angle_next_left))
        
        x_start_right, y_start_right = x_right[0], y_right[0]
        x_start_next_left, y_start_next_left = x_next_left[0], y_next_left[0]
        
        theta_right = np.arctan2(y_start_right, x_start_right)
        theta_next_left = np.arctan2(y_start_next_left, x_start_next_left)
        
        if theta_next_left < theta_right:
            theta_next_left += 2 * np.pi
            
        x_root_right = r_r * np.cos(theta_right)
        y_root_right = r_r * np.sin(theta_right)
        x_root_next_left = r_r * np.cos(theta_next_left)
        y_root_next_left = r_r * np.sin(theta_next_left)
        
        right_root_line_x = np.linspace(x_root_right, x_start_right, 10)
        right_root_line_y = np.linspace(y_root_right, y_start_right, 10)
        for x, y in zip(right_root_line_x, right_root_line_y):
            continuous_points.append((x, y, 0.0))
            
        for x, y in zip(x_right, y_right):
            continuous_points.append((x, y, 0.0))
            
        tip_x = np.linspace(x_right[-1], x_next_left[-1], 10)
        tip_y = np.linspace(y_right[-1], y_next_left[-1], 10)
        for x, y in zip(tip_x, tip_y):
            continuous_points.append((x, y, 0.0))
            
        for x, y in zip(x_next_left[::-1], y_next_left[::-1]):
            continuous_points.append((x, y, 0.0))
            
        left_root_line_x = np.linspace(x_start_next_left, x_root_next_left, 10)
        left_root_line_y = np.linspace(y_start_next_left, y_root_next_left, 10)
        for x, y in zip(left_root_line_x, left_root_line_y):
            continuous_points.append((x, y, 0.0))
            
        angle_next_right = next_teeth_angle + offset
        x_start_next_right = x_inv[0] * np.cos(angle_next_right) - y_inv[0] * np.sin(angle_next_right)
        y_start_next_right = x_inv[0] * np.sin(angle_next_right) + y_inv[0] * np.cos(angle_next_right)
        theta_next_right = np.arctan2(y_start_next_right, x_start_next_right)
        
        if theta_next_right < theta_next_left:
            theta_next_right += 2 * np.pi
            
        root_arc_angles = np.linspace(theta_next_left, theta_next_right, 10)
        for angle in root_arc_angles:
            arc_x = r_r * np.cos(angle)
            arc_y = r_r * np.sin(angle)
            continuous_points.append((arc_x, arc_y, 0.0))
            
    return continuous_points

if __name__ == "__main__":
    points = get_continuous_gear_profile(m=12, z=18, pressure_angle=20)
    
    print(f"Generated {len(points)} continuous 3D points.")
    
    points = np.array(points)
    
    plt.figure(figsize=(8, 8))
    plt.plot(points[:, 0], points[:, 1], color='blue', linewidth=1.5)
    
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.title("Spur Gear Profile — Scatter Plot")
    plt.axis("equal")
    plt.grid(True)
    plt.show()