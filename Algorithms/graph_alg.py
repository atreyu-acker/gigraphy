import numpy as np

difficulty_map = {
    "Beginner": ["linear", "linear"],
    "Easy":     ["linear", "linear", "quadratic"],
    "Medium":   ["linear", "linear", "quadratic", "quadratic"],
    "Hard":     ["linear", "linear", "quadratic", "quadratic", "quadratic"],
    "Expert":   ["quadratic", "quadratic", "quadratic", "quadratic", "quadratic"],
}

SECTION_WIDTH = 25

def generate_linear_section(x_start, x_end, y_start):
    y_end = np.random.randint(0, 51)
    m = round((y_end - y_start) / (x_end - x_start), 2)
    c = round(y_start - m * x_start, 2)
    return {
        "x_start": x_start,
        "x_end": x_end,
        "y_start": y_start,
        "y_end": y_end,
        "coefficients": {"m": m, "c": c},
        "equation_type": "linear"
    }

"""def generate_quadratic_section(x_start, x_end, y_start):
    section_width = x_end - x_start

    # pick vertex position in local coordinates
    vertex_x = np.random.randint(5, section_width - 5)
    
    # pick a so curve is visible but not too steep
    a = np.random.choice([0.05, 0.1, 0.15, -0.05, -0.1, -0.15])

    # vertex y is constrained so curve stays roughly visible
    # for upward curve vertex should be below y_start
    # for downward curve vertex should be above y_start
    if a > 0:
        vertex_y = np.random.randint(max(0, int(y_start) - 20), int(y_start) + 5)
    else:
        vertex_y = np.random.randint(int(y_start) - 5, min(50, int(y_start) + 20))

    # expand y = a(x - vertex_x)^2 + vertex_y
    # = ax^2 - 2a*vertex_x*x + a*vertex_x^2 + vertex_y
    b = round(-2 * a * vertex_x, 2)
    c = round(a * vertex_x**2 + vertex_y, 2)

    # generate curve in local coordinates
    x_values = np.linspace(0, section_width, 300)
    y_values = a * x_values**2 + b * x_values + c

    # y_start is the value at x=0 in local coords which is just c
    # adjust c so curve starts at y_start
    y_offset = y_start - float(a * 0**2 + b * 0 + c)
    # which simplifies to:
    y_offset = y_start - c
    
    # apply offset to c and vertex_y
    c = round(c + y_offset, 2)
    vertex_y = round(vertex_y + y_offset, 2)

    # recalculate y_values with corrected c
    y_values = a * x_values**2 + b * x_values + c

    # calculate actual roots from corrected equation
    discriminant = b**2 - 4 * a * c
    roots = []
    if discriminant >= 0:
        root1 = round((-b + np.sqrt(discriminant)) / (2 * a), 2)
        root2 = round((-b - np.sqrt(discriminant)) / (2 * a), 2)
        roots = [root1, root2]

    y_end = round(float(a * section_width**2 + b * section_width + c), 2)

    return {
        "x_start": x_start,
        "x_end": x_end,
        "y_start": y_start,
        "y_end": y_end,
        "x_values": x_values + x_start,
        "y_values": y_values,
        "coefficients": {"a": a, "b": b, "c": c},
        "roots": roots,
        "vertex": (round(vertex_x + x_start, 2), round(vertex_y, 2)),
        "equation_type": "quadratic"
    }

"""

def generate_quadratic_section(x_start, x_end, y_start):
    section_width = x_end - x_start

    if x_start == 0:
        root1 = 0
    else:
        root1 = np.random.randint(2, section_width - 2)

    root2 = np.random.randint(2, section_width - 2)
    
    while root2 == root1:
        root2 = np.random.randint(2, section_width - 2)

    a = np.random.choice([0.1, 0.2, -0.1, -0.2])
    b = round(-a * (root1 + root2), 2)
    c = round(a * root1 * root2, 2)
    
    x_values = np.linspace(0, section_width, 300)
    y_values = a * x_values**2 + b * x_values + c

    y_offset = y_start - c                # we need an x offset because the roots are not in the right place.
    y_values = y_values + y_offset
    c = round(c + y_offset, 2)
    
    y_end = round(float(a * section_width**2 + b * section_width + c), 2)
    
    print(f"Generated roots: {root1}, {root2}")
    print(f"a={a}, b={b}, c={c}")
    print(f"y at root1: {a * root1**2 + b * root1 + c}")
    print(f"y at root2: {a * root2**2 + b * root2 + c}")
    
    return {
        "x_start": x_start,
        "x_end": x_end,
        "y_start": y_start,
        "y_end": y_end,
        "x_values": x_values + x_start,
        "y_values": y_values,
        "coefficients": {"a": a, "b": b, "c": c},
        "roots": [root1, root2],
        "equation_type": "quadratic"
    }



def generate_level(difficulty):
    equation_types = difficulty_map[difficulty]

    np.random.shuffle(equation_types)
    
    sections = []
    y_current = np.random.randint(0, 26)
    section_width = 25  
    
    for i, eq_type in enumerate(equation_types):
        x_start = i * section_width
        x_end = (i + 1) * section_width
        
        if eq_type == "linear":
            section = generate_linear_section(x_start, x_end, y_current)
        elif eq_type == "quadratic":
            section = generate_quadratic_section(x_start, x_end, y_current)
        
        sections.append(section)
        y_current = section["y_end"]

    return sections



def extend_linear(ax, m, c, x_from, x_to, color):
    y_from = m * x_from + c
    y_to = m * x_to + c
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
        m = section["coefficients"]["m"]
        c = section["coefficients"]["c"]

        
        if section["x_start"] == 0:
            points.append((0, round(c, 2)))

        
        if m != 0:
            x_int = round(-c / m, 2)
            points.append((x_int, 0))

        
        points.append((section["x_start"], section["y_start"]))

    elif section["equation_type"] == "quadratic":
        a = section["coefficients"]["a"]
        b = section["coefficients"]["b"]
        c = section["coefficients"]["c"]

        
        if section["x_start"] == 0:
            points.append((0, round(c, 2)))

        
        for root in section["roots"]:
            global_root = round(root + section["x_start"], 2)
            points.append((global_root, 0))

        
        turning_x_local = round(-b / (2 * a), 2)
        turning_x_global = round(turning_x_local + section["x_start"], 2)
        turning_y = round(float(
            a * turning_x_local**2 + b * turning_x_local + c
        ), 2)
        points.append((turning_x_global, turning_y))

        
        points.append((section["x_start"], section["y_start"]))

    return points

