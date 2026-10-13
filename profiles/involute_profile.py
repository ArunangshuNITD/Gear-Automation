import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def generate_profile_report(m, z, pressure_angle):
    r_p = m * z / 2
    phi = np.radians(pressure_angle)
    r_b = r_p * math.cos(phi)
    r_a = r_p + m
    r_r = r_p - (1.25 * m)

    lines = []
    lines.append("                 GEAR PROFILE CALCULATION REPORT")
    lines.append("=" * 68)
    lines.append(f"Module m                     : {m} mm")
    lines.append(f"Number of teeth z            : {z}")
    lines.append(f"Pressure angle               : {pressure_angle} deg")
    lines.append(f"Pitch circle radius         : {r_p:.4f} mm")
    lines.append(f"Base circle radius          : {r_b:.4f} mm")
    lines.append(f"Addendum circle radius      : {r_a:.4f} mm")
    lines.append(f"Root circle radius          : {r_r:.4f} mm")
    lines.append(f"Pitch diameter              : {2 * r_p:.4f} mm")
    lines.append(f"Base diameter               : {2 * r_b:.4f} mm")
    lines.append(f"Addendum diameter           : {2 * r_a:.4f} mm")
    lines.append(f"Root diameter               : {2 * r_r:.4f} mm")
    lines.append("")
    lines.append("Profile geometry summary:")
    lines.append(f"Circular pitch              : {(math.pi * m):.4f} mm")
    lines.append(f"Tooth thickness at pitch    : {(math.pi * m / 2):.4f} mm")
    lines.append(f"Involute start parameter    : {math.sqrt((r_a / r_b) ** 2 - 1):.4f}")
    lines.append("=" * 68)

    return {"m": m, "z": z, "pressure_angle": pressure_angle, "report": "\n".join(lines)}


def generate_involute_profile(m, z, pressure_angle):
    report = generate_profile_report(m, z, pressure_angle)
    r_p = m * z / 2
    phi = np.radians(pressure_angle)
    r_b = r_p * math.cos(phi)
    r_a = r_p + m
    r_r = r_p - (1.25 * m)

    print(f"pitch circle radius: {r_p}")
    print(f'base radius :{r_b}')
    print(f'addendum cicle radius: {r_a}')
    print(f'root circle radius: {r_r}')

    angles = np.linspace(0, 2 * np.pi, 360)
    x_p = r_p * np.cos(angles)
    y_p = r_p * np.sin(angles)
    x_b = r_b * np.cos(angles)
    y_b = r_b * np.sin(angles)
    x_a = r_a * np.cos(angles)
    y_a = r_a * np.sin(angles)
    x_r = r_r * np.cos(angles)
    y_r = r_r * np.sin(angles)

    t_max = math.sqrt((r_a / r_b) ** 2 - 1)
    t = np.linspace(0, t_max, 100)

    inv_phi = np.tan(phi) - phi
    offset = (np.pi / (2 * z)) - inv_phi

    x_inv = r_b * (np.cos(t) + (t * np.sin(t)))
    y_inv = r_b * (np.sin(t) - (t * np.cos(t)))

    pitch_color = '#b8c5d9'
    base_color = '#d9d3bd'
    addendum_color = '#c7d9c1'
    root_color = '#d9c1c1'
    involute_color = 'steelblue'

    plt.plot(x_p, y_p, label='Pitch circle', linestyle='--', color=pitch_color, alpha=0.9)
    plt.plot(x_b, y_b, label='base circle', linestyle='--', color=base_color, alpha=0.9)
    plt.plot(x_a, y_a, label='addendum circle', linestyle='--', color=addendum_color, alpha=0.9)
    plt.plot(x_r, y_r, label='root circle', linestyle='--', color=root_color, alpha=0.9)

    right_tips = []
    left_tips = []

    for i in range(z):
        teeth_angle = i * 2 * np.pi / z
        angle_right = teeth_angle + offset
        angle_left = teeth_angle - offset

        x_right = (x_inv * np.cos(angle_right)) - (y_inv * np.sin(angle_right))
        y_right = (x_inv * np.sin(angle_right)) + (y_inv * np.cos(angle_right))
        x_left = (x_inv * np.cos(angle_left)) + (y_inv * np.sin(angle_left))
        y_left = (x_inv * np.sin(angle_left)) - (y_inv * np.cos(angle_left))

        x_start_right = x_right[0]
        y_start_right = y_right[0]
        x_start_left = x_left[0]
        y_start_left = y_left[0]

        theta_right = np.arctan2(y_start_right, x_start_right)
        theta_left = np.arctan2(y_start_left, x_start_left)

        x_root_right = r_r * np.cos(theta_right)
        y_root_right = r_r * np.sin(theta_right)
        x_root_left = r_r * np.cos(theta_left)
        y_root_left = r_r * np.sin(theta_left)

        right_tips.append((x_right[-1], y_right[-1]))
        left_tips.append((x_left[-1], y_left[-1]))

        plt.plot(x_right, y_right, color=involute_color, linewidth=2)
        plt.plot(x_left, y_left, color=involute_color, linewidth=2)
        plt.plot(
            np.linspace(x_start_right, x_root_right, 100),
            np.linspace(y_start_right, y_root_right, 100),
            color=involute_color,
            linewidth=2,
        )
        plt.plot(
            np.linspace(x_start_left, x_root_left, 100),
            np.linspace(y_start_left, y_root_left, 100),
            color=involute_color,
            linewidth=2,
        )
        plt.plot([x_root_left, x_root_right], [y_root_left, y_root_right], color=involute_color, linewidth=2)

    for i in range(z):
        x1, y1 = right_tips[i]
        x2, y2 = left_tips[(i + 1) % z]
        plt.plot([x1, x2], [y1, y2], color=involute_color, linewidth=2)

    plt.tight_layout()
    plt.axis('Equal')
    plt.legend(loc='upper left')

    figures_dir = Path(__file__).resolve().parent.parent / 'figures'
    figures_dir.mkdir(exist_ok=True)
    save_path = figures_dir / 'gear_profile.png'
    plt.savefig(save_path)
    print(f"Saved profile image to: {save_path}")
    print(report["report"])
    plt.show()


if __name__ == "__main__":
    generate_involute_profile(m=12, z=18, pressure_angle=20)