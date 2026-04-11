import numpy as np

difficulty_sections = {
    "Beginner": 2,
    "Easy":     3,
    "Medium":   4,
    "Hard":     5,
    "Expert":   5,
}

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


difficulty_map = {
    "Beginner": ["linear", "linear"],
    "Easy":     ["linear", "linear", "quadratic"],
    "Medium":   ["linear", "linear", "quadratic", "quadratic"],
    "Hard":     ["linear", "linear", "quadratic", "quadratic", "quadratic"],
    "Expert":   ["quadratic", "quadratic", "quadratic", "quadratic", "quadratic"],
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


def draw_sections(sections, active_section=0):
    num = len(sections)
    fig, axes = plt.subplots(1, num, figsize=(3 * num, 4))
    
    if num == 1:
        axes = [axes]  # make iterable if only one section
    
    for i, (section, ax) in enumerate(zip(sections, axes)):
        # draw the curve
        if section["equation_type"] == "linear":
            ax.plot(
                [0, section["section_width"]],
                [section["y_start"], section["y_end"]],
                color=colors[i],
                linewidth=2
            )
        elif section["equation_type"] == "quadratic":
            ax.plot(
                section["x_values"],  # already local 0 to section_width
                section["y_values"],
                color=colors[i],
                linewidth=2
            )
        
        # set axis limits
        ax.set_xlim(0, section["section_width"])
        ax.set_ylim(y_min, y_max)
        ax.axhline(0, color="black", linewidth=0.8)
        ax.grid(True, alpha=0.3)
        
        # show y axis only for active and completed sections
        if i <= active_section:
            ax.axvline(0, color="black", linewidth=0.8)
            ax.yaxis.set_visible(True)
        else:
            ax.yaxis.set_visible(False)
        
        # dots and annotations only for active section
        if i == active_section:
            points = calculate_significant_points(section)
            for px, py in points:
                ax.plot(px, py, 'o', color="black", markersize=4, zorder=5)
                ax.annotate(
                    f"({round(px, 1)}, {round(py, 1)})",
                    xy=(px, py),
                    xytext=(0, 10),
                    textcoords="offset points",
                    fontsize=8,
                    ha="center",
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="white", alpha=0.8)
                )
    
    return fig, axes


    return all_significant_points