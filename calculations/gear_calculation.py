import math


def calculate_gear_design():
    # ======================== INPUT PARAMETERS ========================

    power = 30  # kW
    N_p = 250  # rpm
    i = 4

    sigma_b_allowable_pinion = 750  # MPa
    sigma_b_allowable_gear = 580  # MPa

    E1 = 2.1 * 10**5  # MPa
    E2 = 2.1 * 10**5  # MPa

    pressure_angle = 20  # degrees
    cs = 1.5
    Fos = 3
    BHN = 300

    X = 10  # Face width factor: b = X*m

    # Standard module series used for this project.
    standard_modules = [
        0.5, 0.8, 1, 1.25, 1.5, 2, 2.5, 3, 4, 5,
        6, 8, 10, 12, 16, 20, 25, 32, 40, 50
    ]

    lines = []

    def add_line(text=""):
        lines.append(str(text))

    def add_section(title):
        add_line()
        add_line("=" * 68)
        add_line(title)
        add_line("=" * 68)

    def fmt(value, digits=3):
        return f"{value:,.{digits}f}"

    # ======================== BASIC CALCULATIONS ========================

    phi = math.radians(pressure_angle)

    Z_min = 2 / (math.sin(phi) ** 2)
    Z_p = math.ceil(Z_min)
    Z_g = i * Z_p
    N_g = N_p / i

    so_p = sigma_b_allowable_pinion / Fos
    so_g = sigma_b_allowable_gear / Fos

    Y_p = 0.484 - (3.28 / Z_p)
    Y_g = 0.484 - (3.28 / Z_g)

    if so_p * Y_p <= so_g * Y_g:
        weaker_member = "Pinion"
        so = so_p
        Y = Y_p
        Z = Z_p
        N = N_p
    else:
        weaker_member = "Gear"
        so = so_g
        Y = Y_g
        Z = Z_g
        N = N_g

    T_p = cs * power * 60 * 10**6 / (2 * math.pi * N_p)

    # ======================== ITERATIVE MODULE CALCULATION ========================

    cv = 0.5
    tolerance = 1e-5
    m_prev = 100.0
    m_required = 0.0
    max_itr = 100
    itr = 0
    iteration_rows = []

    while abs(m_prev - m_required) > tolerance and itr < max_itr:
        m_prev = m_required

        m_required = (2 * T_p / (so * X * cv * Y * Z)) ** (1 / 3)

        V = math.pi * m_required * Z * N / 60000
        cv = 3 / (3 + V)

        itr += 1
        iteration_rows.append((itr, m_required, V, cv))

    if itr >= max_itr and abs(m_prev - m_required) > tolerance:
        raise RuntimeError("Module iteration did not converge.")

    # ======================== STANDARD MODULE AND STRENGTH CHECKS ========================

    start_idx = 0
    while (
        start_idx < len(standard_modules)
        and standard_modules[start_idx] < m_required
    ):
        start_idx += 1

    selected = None
    strength_rows = []

    for candidate_m in standard_modules[start_idx:]:
        D_p_candidate = candidate_m * Z_p
        D_g_candidate = candidate_m * Z_g
        b_candidate = X * candidate_m

        V_candidate = math.pi * candidate_m * Z * N / 60000
        cv_candidate = 3 / (3 + V_candidate)

        F_t_candidate = 2 * T_p / D_p_candidate
        F_d_candidate = F_t_candidate / cv_candidate

        S_b_candidate = candidate_m * b_candidate * so * Y
        bending_ok = S_b_candidate >= F_t_candidate

        Q = 2 * Z_g / (Z_p + Z_g)
        s_enc = 2.8 * BHN - 70
        K = (
            (s_enc**2 * math.sin(phi) / 1.4)
            * ((1 / E1) + (1 / E2))
        )

        F_w_candidate = D_p_candidate * b_candidate * K * Q
        wear_required = 1.2 * F_d_candidate
        wear_ok = F_w_candidate >= wear_required

        strength_rows.append(
            (
                candidate_m,
                S_b_candidate,
                F_t_candidate,
                bending_ok,
                F_w_candidate,
                wear_required,
                wear_ok,
            )
        )

        if bending_ok and wear_ok:
            selected = {
                "m": candidate_m,
                "D_p": D_p_candidate,
                "D_g": D_g_candidate,
                "b": b_candidate,
                "V": V_candidate,
                "cv": cv_candidate,
                "F_t": F_t_candidate,
                "F_d": F_d_candidate,
                "S_b": S_b_candidate,
                "Q": Q,
                "s_enc": s_enc,
                "K": K,
                "F_w": F_w_candidate,
                "wear_required": wear_required,
                "bending_ok": bending_ok,
                "wear_ok": wear_ok,
            }
            break

    # ======================== BUILD REPORT ========================

    add_line("                 SPUR GEAR DESIGN CALCULATION REPORT")
    add_line("=" * 68)

    add_section("1. INPUT PARAMETERS")
    add_line(f"Power                         : {power} kW")
    add_line(f"Pinion speed                  : {N_p} rpm")
    add_line(f"Gear ratio                    : {i}:1")
    add_line(f"Pinion allowable stress       : {sigma_b_allowable_pinion} MPa")
    add_line(f"Gear allowable stress         : {sigma_b_allowable_gear} MPa")
    add_line(f"Young's modulus E1            : {E1:,.0f} MPa")
    add_line(f"Young's modulus E2            : {E2:,.0f} MPa")
    add_line(f"Pressure angle                : {pressure_angle} degrees")
    add_line(f"Service factor                : {cs}")
    add_line(f"Factor of safety              : {Fos}")
    add_line(f"Brinell hardness number       : {BHN}")
    add_line(f"Face width factor X           : {X}")

    add_section("2. TOOTH NUMBERS AND SPEEDS")
    add_line(f"Minimum pinion teeth           : {fmt(Z_min)}")
    add_line(f"Selected pinion teeth Zp      : {Z_p}")
    add_line(f"Gear teeth Zg                 : {Z_g}")
    add_line(f"Gear speed                    : {fmt(N_g)} rpm")
    add_line(f"Pinion Lewis factor Yp        : {fmt(Y_p, 5)}")
    add_line(f"Gear Lewis factor Yg          : {fmt(Y_g, 5)}")
    add_line(f"Pinion design stress so_p     : {fmt(so_p)} MPa")
    add_line(f"Gear design stress so_g       : {fmt(so_g)} MPa")
    add_line(f"Weaker member                 : {weaker_member}")
    add_line(f"Selected design stress so     : {fmt(so)} MPa")
    add_line(f"Selected Lewis factor Y       : {fmt(Y, 5)}")

    add_section("3. TORQUE")
    add_line(f"Design torque on pinion       : {fmt(T_p)} N-mm")

    add_section("4. ITERATIVE MODULE CALCULATION")
    add_line(f"{'Iter.':<8}{'Module (mm)':>16}{'Velocity (m/s)':>20}{'Cv':>12}")
    add_line("-" * 56)
    for row_itr, row_m, row_V, row_cv in iteration_rows:
        add_line(
            f"{row_itr:<8}{row_m:>16.5f}{row_V:>20.5f}{row_cv:>12.5f}"
        )
    add_line("-" * 56)
    add_line(f"Calculated minimum module     : {fmt(m_required, 5)} mm")

    add_section("5. STANDARD MODULE AND STRENGTH CHECKS")
    add_line(
        f"{'m (mm)':>8} {'Bending cap.':>15} {'Ft':>12} "
        f"{'Bending':>12} {'Wear cap.':>14} {'1.2Fd':>12} {'Wear':>9}"
    )
    add_line("-" * 91)

    for row in strength_rows:
        (
            test_m,
            S_b_test,
            F_t_test,
            bending_test,
            F_w_test,
            wear_req_test,
            wear_test,
        ) = row

        add_line(
            f"{test_m:>8.3f} {S_b_test:>15.2f} {F_t_test:>12.2f} "
            f"{('PASS' if bending_test else 'FAIL'):>12} "
            f"{F_w_test:>14.2f} {wear_req_test:>12.2f} "
            f"{('PASS' if wear_test else 'FAIL'):>9}"
        )

    add_line("-" * 91)

    if selected is None:
        add_line("DESIGN STATUS: No available standard module passed both checks.")
        add_line("Add larger standard modules or review the design inputs.")
        return {
            "m": None,
            "z": Z_p,
            "pressure_angle": pressure_angle,
            "report": "\n".join(lines),
        }

    add_section("6. FINAL SELECTED DESIGN")
    add_line(f"Selected standard module       : {fmt(selected['m'])} mm")
    add_line(f"Pinion pitch diameter Dp       : {fmt(selected['D_p'])} mm")
    add_line(f"Gear pitch diameter Dg         : {fmt(selected['D_g'])} mm")
    add_line(f"Face width b                   : {fmt(selected['b'])} mm")
    add_line(f"Pitch-line velocity            : {fmt(selected['V'])} m/s")
    add_line(f"Velocity factor Cv             : {fmt(selected['cv'], 5)}")
    add_line(f"Tangential force Ft            : {fmt(selected['F_t'])} N")
    add_line(f"Dynamic load Fd                : {fmt(selected['F_d'])} N")

    add_section("7. BENDING CHECK")
    add_line(f"Bending capacity Sb            : {fmt(selected['S_b'])} N")
    add_line(f"Tangential force Ft            : {fmt(selected['F_t'])} N")
    add_line(
        "Bending criteria               : "
        + ("SATISFIED" if selected["bending_ok"] else "NOT SATISFIED")
    )

    add_section("8. WEAR CHECK")
    add_line(f"Relative wheel factor Q        : {fmt(selected['Q'], 5)}")
    add_line(f"Surface endurance value        : {fmt(selected['s_enc'])} MPa")
    add_line(f"Wear factor K                  : {selected['K']:.8e}")
    add_line(f"Wear capacity Fw               : {fmt(selected['F_w'])} N")
    add_line(f"Required wear load 1.2Fd       : {fmt(selected['wear_required'])} N")
    add_line(
        "Wear criteria                  : "
        + ("SATISFIED" if selected["wear_ok"] else "NOT SATISFIED")
    )

    add_section("9. FINAL RESULT")
    add_line("Both bending and wear criteria are satisfied.")
    add_line(f"Recommended standard module: {fmt(selected['m'])} mm")
    add_line()
    add_line("Note: Verify the selected standard-module series and material")
    add_line("properties against your course/design specification.")

    return {
        "m": selected["m"],
        "z": Z_p,
        "pressure_angle": pressure_angle,
        "report": "\n".join(lines),
    }


def generate_report():
    return calculate_gear_design()["report"]


if __name__ == "__main__":
    result = calculate_gear_design()
    print(result["report"])
