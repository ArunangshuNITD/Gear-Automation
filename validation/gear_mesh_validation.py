from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from calculations.gear_calculation import calculate_gear_design


# You can call this directly from this module.
# Example: result = calculate_gear_design()

def validate_gear_mesh(d):
    required_key=['m','Z_p','Z_g','D_p','D_g','i']
    if not all(key in d for key in required_key):
        print('missing parameters')
        return {"overall_pass":False}
    if any(d[key] is None for key in required_key):
        print('Some parameters have no value')
        return {"overall_pass":False}
    m=d['m']
    Z_p=d['Z_p']
    D_p=d['D_p']
    D_g=d['D_g']
    Z_g=d['Z_g']
    i=d['i']
    
    checks={
          "pinion_pitch_diameter": False,
            "gear_pitch_diameter": False,
            "transmission_ratio": False,
    }
    if Z_p <= 0 or Z_g <= 0 or m<=0 or i<=0 or D_p<=0 or D_g<=0:
        print("Invalid gear parameters")
        checks['overall_pass']=False
        return checks
    if abs(m*Z_p-D_p)<1e-6: # Allow a tiny numerical difference due to floating-point rounding.
        print('Pinion pitch diameter: PASS')
        checks['pinion_pitch_diameter']=True
    else:
        print('Pinion pitch diameter failed')
        
    if abs(m*Z_g-D_g)<1e-6:
            print('Gear pitch diameter: PASS')
            checks['gear_pitch_diameter']=True
    else:
            print('Gear pitch diameter failed')
    if abs(i-(Z_g/Z_p))<1e-6:
        print('Transmission ratio: PASS')
        checks['transmission_ratio']=True
    else:
        print('Transmission ratio failed')
    checks['overall_pass']=all(checks.values())
    return checks


def build_mesh_validation_report(d, checks=None):
    if checks is None:
        checks = validate_gear_mesh(d)

    required = {
        'm': d.get('m'),
        'Z_p': d.get('Z_p'),
        'Z_g': d.get('Z_g'),
        'D_p': d.get('D_p'),
        'D_g': d.get('D_g'),
        'i': d.get('i'),
    }

    lines = []
    lines.append("                 GEAR MESH VALIDATION REPORT")
    lines.append("=" * 68)
    lines.append("Input parameters:")
    for key, value in required.items():
        lines.append(f"{key:<18}: {value}")

    lines.append("")
    lines.append("Checks:")
    lines.append(f"{'Pinion pitch diameter':<30}: {'PASS' if checks.get('pinion_pitch_diameter') else 'FAIL'}")
    lines.append(f"{'Gear pitch diameter':<30}: {'PASS' if checks.get('gear_pitch_diameter') else 'FAIL'}")
    lines.append(f"{'Transmission ratio':<30}: {'PASS' if checks.get('transmission_ratio') else 'FAIL'}")
    lines.append("-" * 68)
    lines.append(f"Overall result: {'PASS' if checks.get('overall_pass') else 'FAIL'}")
    lines.append("=" * 68)

    if not checks.get('overall_pass', False):
        lines.append("Status: Gear mesh does not satisfy the required geometry conditions.")
    else:
        lines.append("Status: Gear mesh geometry is valid and ready for profile generation.")

    return "\n".join(lines)


if __name__ == "__main__":
    result = calculate_gear_design()
    # print(type(result))
    test_data = {
        "m": 2,
        "Z_p": 20,
        "Z_g": 40,
        "D_p": 41,  # Incorrect: m * Z_p = 2 * 20 = 40
        "D_g": 80,
        "i": 2,
    }
    print(validate_gear_mesh(test_data))
    print(build_mesh_validation_report(test_data))


