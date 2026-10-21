
import sys
from pathlib import Path

import math
import matplotlib.pyplot as plt

# Add the project root to Python's import path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from profiles.involute_profile import generate_involute_profile
from calculations.gear_calculation import calculate_gear_design


res = calculate_gear_design()

# read keys robustly (support both lowercase and uppercase return keys)
weaker_member = res.get('weaker member')
i = res.get('i', 1)
m = res.get('m')
pressure_angle = res.get('pressure_angle', res.get('pressure angle', 20))

# pinion teeth: returned as 'Z_p' or 'z'
Z_p = int(res.get('Z_p', res.get('z', 0)))
# gear teeth: use returned 'Z_g' if present, otherwise derive from ratio
Z_g = int(res.get('Z_g', Z_p * i))

# pitch diameters (use returned if available)
D_p = res.get('D_p', m * Z_p)
D_g = res.get('D_g', m * Z_g)

print(f"{D_p},{D_g}")


center_to_center_dist = m * (Z_p + Z_g) / 2
print(center_to_center_dist)

gear_rotation = math.pi - math.pi / Z_g if Z_g != 0 else 0.0
print(f"gear_rotation: {gear_rotation}")

fig,ax=plt.subplots()
ax.plot(0,0,color='black',marker='x')
ax.plot(center_to_center_dist,0,color='black',marker='x')
ax.plot((0,center_to_center_dist),(0,0),color='gray',linestyle='--')
pinion = generate_involute_profile(
	m,
	Z_p,
	pressure_angle,
	ax=ax,
	involute_color='crimson',
	rotation=0.0,
)

gear = generate_involute_profile(
	m,
	Z_g,
	pressure_angle,
	ax=ax,
	center=(center_to_center_dist, 0),
	involute_color='navy',
	rotation=gear_rotation,
)
ax.set_aspect('equal',adjustable='datalim')

# ensure figures directory exists and save the composed gear-pair image
figures_dir = Path(__file__).resolve().parent.parent / 'figures'
figures_dir.mkdir(exist_ok=True)
save_path = figures_dir / 'gear_pair.png'
fig.savefig(save_path, dpi=300, bbox_inches='tight')
print(f"Saved gear pair image to: {save_path}")

plt.show()