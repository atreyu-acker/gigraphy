import numpy as np

difficulty_map = {
    "Beginner": ["linear", "linear"],
    "Easy":     ["linear", "linear", "quadratic"],
    "Medium":   ["linear", "linear", "quadratic", "quadratic"],
    "Hard":     ["linear", "linear", "quadratic", "quadratic", "quadratic"],
    "Expert":   ["quadratic", "quadratic", "quadratic", "quadratic", "quadratic"],
}

SECTION_WIDTH = 25
ROOT_MARGIN = 2
QUADRATIC_Y_MIN = -20
QUADRATIC_Y_MAX = 70
MAX_QUADRATIC_ATTEMPTS = 100
QUADRATIC_A_MAGNITUDES = [0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]
LOW_A_VERTEX_MAGNITUDES = set(QUADRATIC_A_MAGNITUDES[: len(QUADRATIC_A_MAGNITUDES) // 2])

def generate_linear_section(x_start, x_end, y_start):
    section_width = x_end - x_start
    y_end = np.random.randint(0, 51)
    m = round((y_end - y_start) / section_width, 2)
    c = round(float(y_start), 2)
    return {
        "x_start": x_start,
        "x_end": x_end,
        "y_start": y_start,
        "y_end": y_end,
        "coefficients": {"m": m, "c": c},
        "equation_type": "linear"
    }

def generate_quadratic_section(x_start, x_end, y_start):
    section_width = x_end - x_start
    root_low = ROOT_MARGIN
    root_high = section_width - ROOT_MARGIN
    x_values = np.linspace(0, section_width, 300)

    def in_bounds(a_val, b_val, c_val):
        probe_x = [0.0, float(section_width)]
        turning_x = -b_val / (2 * a_val)
        if 0 <= turning_x <= section_width:
            probe_x.append(float(turning_x))
        probe_y = [a_val * x**2 + b_val * x + c_val for x in probe_x]
        return min(probe_y) >= QUADRATIC_Y_MIN and max(probe_y) <= QUADRATIC_Y_MAX

    low_pool = [v for v in QUADRATIC_A_MAGNITUDES if v in LOW_A_VERTEX_MAGNITUDES]
    high_pool = [v for v in QUADRATIC_A_MAGNITUDES if v not in LOW_A_VERTEX_MAGNITUDES]
    target_formula_type = str(np.random.choice(["quadratic_vertex", "quadratic_standard"]))
    target_pool = low_pool if target_formula_type == "quadratic_vertex" else high_pool
    alternate_pool = high_pool if target_formula_type == "quadratic_vertex" else low_pool

    def try_generate_for_pool(magnitude_pool):
        for _ in range(MAX_QUADRATIC_ATTEMPTS):
            if x_start == 0:
                root1 = 0
            else:
                root1 = np.random.randint(root_low, root_high)

            root2 = np.random.randint(root_low, root_high)
            while root2 == root1:
                root2 = np.random.randint(root_low, root_high)

            a_mag = float(np.random.choice(magnitude_pool))
            a_sign = int(np.random.choice([-1, 1]))
            a = round(a_mag * a_sign, 2)
            b = round(-a * (root1 + root2), 2)
            c = round(a * root1 * root2, 2)

            y_offset = y_start - c
            c = round(c + y_offset, 2)
            if not in_bounds(a, b, c):
                continue

            y_end = round(float(a * section_width**2 + b * section_width + c), 2)
            y_values = a * x_values**2 + b * x_values + c

            discriminant = b**2 - 4 * a * c
            roots = []
            if discriminant >= 0:
                sqrt_disc = np.sqrt(discriminant)
                roots = [
                    float((-b + sqrt_disc) / (2 * a)),
                    float((-b - sqrt_disc) / (2 * a)),
                ]

            if a_mag in LOW_A_VERTEX_MAGNITUDES:
                q_exact = b / (2 * a)
                p_exact = c - a * (q_exact**2)
                answer_coefficients = {
                    "a": round(a, 2),
                    "q": round(float(q_exact), 2),
                    "p": round(float(p_exact), 2),
                }
                formula_type = "quadratic_vertex"
            else:
                answer_coefficients = {"a": a, "b": b, "c": c}
                formula_type = "quadratic_standard"

            return {
                "x_start": x_start,
                "x_end": x_end,
                "y_start": y_start,
                "y_end": y_end,
                "x_values": x_values + x_start,
                "y_values": y_values,
                "coefficients": {"a": a, "b": b, "c": c},
                "answer_coefficients": answer_coefficients,
                "formula_type": formula_type,
                "roots": roots,
                "equation_type": "quadratic"
            }
        return None

    generated = try_generate_for_pool(target_pool)
    if generated is not None:
        return generated

    generated = try_generate_for_pool(alternate_pool)
    if generated is not None:
        return generated

    fallback_a = 0.2
    fallback_r1, fallback_r2 = 8, 17
    b = round(-fallback_a * (fallback_r1 + fallback_r2), 2)
    c = round(fallback_a * fallback_r1 * fallback_r2, 2)
    c = round(c + (y_start - c), 2)
    y_end = round(float(fallback_a * section_width**2 + b * section_width + c), 2)
    y_values = fallback_a * x_values**2 + b * x_values + c
    discriminant = b**2 - 4 * fallback_a * c
    roots = []
    if discriminant >= 0:
        sqrt_disc = np.sqrt(discriminant)
        roots = [
            float((-b + sqrt_disc) / (2 * fallback_a)),
            float((-b - sqrt_disc) / (2 * fallback_a)),
        ]
    q_exact = b / (2 * fallback_a)
    p_exact = c - fallback_a * (q_exact**2)
    return {
        "x_start": x_start,
        "x_end": x_end,
        "y_start": y_start,
        "y_end": y_end,
        "x_values": x_values + x_start,
        "y_values": y_values,
        "coefficients": {"a": fallback_a, "b": b, "c": c},
        "answer_coefficients": {"a": fallback_a, "q": round(float(q_exact), 2), "p": round(float(p_exact), 2)},
        "formula_type": "quadratic_vertex",
        "roots": roots,
        "equation_type": "quadratic"
    }



def generate_level(difficulty):
    equation_types = difficulty_map[difficulty][:]

    np.random.shuffle(equation_types)
    
    sections = []
    y_current = np.random.randint(0, 26)
    section_width = 25
    
    for i, eq_type in enumerate(equation_types):
        x_start = i * section_width
        x_end = (i + 1) * section_width
        
        if eq_type == "linear":
            section = generate_linear_section(x_start, x_end, y_current)
            section["answer_coefficients"] = dict(section["coefficients"])
            section["formula_type"] = "linear_standard"
        elif eq_type == "quadratic":
            section = generate_quadratic_section(x_start, x_end, y_current)
        
        sections.append(section)
        y_current = section["y_end"]

    return sections



def extend_linear(ax, m, c, x_from, x_to, x_start_global, color):
    y_from = m * (x_from - x_start_global) + c
    y_to = m * (x_to - x_start_global) + c
    ax.plot(
        [x_from, x_to],
        [y_from, y_to],
        color=color,
        linewidth=1,
        linestyle="dashed",
        alpha=0.4
    )
    


def extend_quadratic(ax, a, b, c, x_from, x_to, x_start_global, color):
    x_vals = np.linspace(x_from, x_to, 100)
    x_local = x_vals - x_start_global
    y_vals = a * x_local**2 + b * x_local + c
    ax.plot(
        x_vals, y_vals,
        color=color,
        linewidth=1,
        linestyle="dashed",
        alpha=0.4
    )
    


def calculate_significant_points(section):
    points = []

    if section["equation_type"] == "linear":
        c = section["coefficients"]["c"]

        if section["x_start"] == 0:
            points.append((0, round(c, 2)))

        points.append((section["x_start"], section["y_start"]))
        points.append((section["x_end"], section["y_end"]))

    elif section["equation_type"] == "quadratic":
        a = section["coefficients"]["a"]
        b = section["coefficients"]["b"]
        c = section["coefficients"]["c"]

        
        if section["x_start"] == 0:
            points.append((0, round(c, 2)))

        
        for root in section["roots"]:
            global_root = root + section["x_start"]
            points.append((global_root, 0))

        
        turning_x_local = -b / (2 * a)
        turning_x_global = turning_x_local + section["x_start"]
        turning_y = float(
            a * turning_x_local**2 + b * turning_x_local + c
        )
        points.append((turning_x_global, turning_y))

        
        points.append((section["x_start"], section["y_start"]))

    return points
