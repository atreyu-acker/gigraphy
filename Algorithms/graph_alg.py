import numpy as np

# this is the difficulty map which determines which levels have how many sections with which graphes.
difficulty_map = {
    "Beginner": ["linear", "linear"],
    "Easy":     ["linear", "linear", "quadratic"],
    "Medium":   ["linear", "linear", "quadratic", "quadratic"],
    "Hard":     ["linear", "linear", "quadratic", "quadratic", "quadratic"],
    "Expert":   ["quadratic", "quadratic", "quadratic", "quadratic", "quadratic"],
}

# these are my global variable, however, i have been careful and only have constants that are never changed in the code. 
SECTION_WIDTH = 25 # sets the width of the sections containing the graphs.
ROOT_MARGIN = 2 # this is a border that tries to place roots in visually nice location rather than right on the border of a section.
QUADRATIC_Y_MIN = -20 # the min hight 
QUADRATIC_Y_MAX = 70 # the max hight
MAX_QUADRATIC_ATTEMPTS = 100 # this is the limit of draw attempts before the fallback is used.
QUADRATIC_A_MAGNITUDES = [0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60] # having a list of a values allows me to split them in half to determine the formula.
LOW_A_VERTEX_MAGNITUDES = QUADRATIC_A_MAGNITUDES[: len(QUADRATIC_A_MAGNITUDES) // 2] # a list of the lowest half of the a values. this influences the likelyhood of getting specific formula types.
HIGH_A_VERTEX_MAGNITUDES = QUADRATIC_A_MAGNITUDES[len(QUADRATIC_A_MAGNITUDES) // 2 :] # the top half of the list.


# this function is called by generate_level and returns a dictionary to the variable sections.
def generate_linear_section(x_start, x_end, y_start): 
    y_end = np.random.randint(0, 51) # the randomly generated y_end where the graph ends.
    m = round(float((y_end - y_start) / SECTION_WIDTH), 2) # finds the gradient.
    c = round(float(y_start), 2) # c is the y_start of the graph. 

    # this is the dictionary value returned.
    return {
        "x_start": x_start,
        "x_end": x_end,
        "y_start": y_start,
        "y_end": y_end,
        "coefficients": {"m": m, "c": c},
        "equation_type": "linear"
    }


# this function is also called by generate_level and returns a slightly larger dictionary than the linear.
def generate_quadratic_section(x_start, x_end, y_start):

    # this is a very important line that creates a list of 300 x coordinates between 0 and 25 (the section width).
    # this is used by matplotlib in draw_graphs.
    x_values = np.linspace(0, SECTION_WIDTH, 300)

    # this function checks if the quadratic lies within the y limits and returns True or False.
    def in_bounds(y_values):
        # it takes all y_values to see if the min or max falls ouside the range of the graph.
        if min(y_values) >= QUADRATIC_Y_MIN and max(y_values) <= QUADRATIC_Y_MAX:
            return True
        return False
        
    # this variable picks randomly if the quadratic will be 
    formula_type = str(np.random.choice(["quadratic_vertex", "quadratic_standard"]))
   
    def try_generate_for_pool(formula_type, target):
        for attempts in range(MAX_QUADRATIC_ATTEMPTS):
            print(attempts)
            
            root1 = np.random.randint(ROOT_MARGIN, SECTION_WIDTH - ROOT_MARGIN)
            root2 = np.random.randint(ROOT_MARGIN, SECTION_WIDTH - ROOT_MARGIN)

            while root2 == root1:
                root2 = np.random.randint(ROOT_MARGIN, SECTION_WIDTH - ROOT_MARGIN)

            if formula_type == "quadratic_standard":
                if target == True:
                    a_mag = float(np.random.choice(HIGH_A_VERTEX_MAGNITUDES))
                else:
                    a_mag = float(np.random.choice(LOW_A_VERTEX_MAGNITUDES))
            else:
                if target == True:
                    a_mag = float(np.random.choice(LOW_A_VERTEX_MAGNITUDES))
                else:
                    a_mag = float(np.random.choice(HIGH_A_VERTEX_MAGNITUDES))

            a_sign = int(np.random.choice([-1, 1]))
            a = round(a_mag * a_sign, 2)
            b = round(-a * (root1 + root2), 2)
            c = round(a * root1 * root2, 2)

            y_offset = y_start - c
            c = round(c + y_offset, 2)
            y_values = a * x_values**2 + b * x_values + c

            if not in_bounds(y_values):
                continue

            y_end = round(float(a * SECTION_WIDTH**2 + b * SECTION_WIDTH + c), 2)
            y_values = a * x_values**2 + b * x_values + c

            discriminant = b**2 - 4 * a * c
            roots = []
            if discriminant >= 0:
                sqrt_disc = np.sqrt(discriminant)
                roots = [
                    float((-b + sqrt_disc) / (2 * a)),
                    float((-b - sqrt_disc) / (2 * a)),
                ]

            if formula_type == "quadratic_vertex":
                q_exact = b / (2 * a)
                p_exact = c - a * (q_exact**2)
                answer_coefficients = {
                    "a": round(a, 2),
                    "q": round(float(q_exact), 2),
                    "p": round(float(p_exact), 2),
                }
                
            else:
                answer_coefficients = {"a": a, "b": b, "c": c}

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

    generated = try_generate_for_pool(formula_type, target=True)
    if generated is not None:
        return generated

    generated = try_generate_for_pool(formula_type, target=False)
    if generated is not None:
        return generated

    print("fallback triggered")
    fallback_a = 0.2
    fallback_r1, fallback_r2 = 8, 17
    b = round(-fallback_a * (fallback_r1 + fallback_r2), 2)
    c = round(fallback_a * fallback_r1 * fallback_r2, 2)
    c = round(c + (y_start - c), 2)
    y_end = round(float(fallback_a * SECTION_WIDTH**2 + b * SECTION_WIDTH + c), 2)
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
