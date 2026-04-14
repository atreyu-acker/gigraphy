import matplotlib
matplotlib.use("Agg")
from Algorithms.graph_alg import calculate_significant_points
from Algorithms.graph_alg import extend_linear, extend_quadratic



def draw_sections(ax, sections, active_section=0):
    x_range_end = len(sections) * 25 + 10
    ax.set_xlim(0, x_range_end)

    colors = ["steelblue", "orange", "green", "red", "purple"]

    all_y = []
    all_significant_points = []

    for i, section in enumerate(sections):
        if section["equation_type"] == "linear":
            all_y.extend([section["y_start"], section["y_end"]])
        else:
            all_y.extend(section["y_values"].tolist())

    y_min = min(0, min(all_y) - 5)
    y_max = max(25, max(all_y) + 5)

    ax.set_ylim(y_min, y_max)
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("x", fontsize=10)
    ax.set_ylabel("y", fontsize=10, rotation=0)

    active_x_start = sections[active_section]["x_start"]
    ax.axvline(active_x_start, color="black", linewidth=0.8)

    y_ticks = ax.get_yticks()
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([str(int(t)) if t == int(t) else str(round(t, 1)) for t in y_ticks])

    for i, section in enumerate(sections):
        color = colors[i]

        if section["equation_type"] == "linear":
            m = section["coefficients"]["m"]
            c = section["coefficients"]["c"]
            ax.plot(
                [section["x_start"], section["x_end"]],
                [section["y_start"], section["y_end"]],
                color=color,
                linewidth=2
            )
            if section["x_start"] > active_x_start:
                extend_linear(ax, m, c, active_x_start, section["x_start"], color)
            if section["x_end"] < x_range_end:
                extend_linear(ax, m, c, section["x_end"], x_range_end, color)

        elif section["equation_type"] == "quadratic":
            a = section["coefficients"]["a"]
            b = section["coefficients"]["b"]
            c = section["coefficients"]["c"]

            print(f"Section x_start: {section['x_start']}")
            print(f"Roots (local): {section['roots']}")
            print(f"a={a}, b={b}, c={c}")

            ax.plot(
                section["x_values"],
                section["y_values"],
                color=color,
                linewidth=2
            )
            if section["x_start"] > active_x_start:
                extend_quadratic(ax, a, b, c, active_x_start, section["x_start"], section["x_start"], color)
            if section["x_end"] < x_range_end:
                extend_quadratic(ax, a, b, c, section["x_end"], x_range_end, section["x_start"], color)

        
        if i == active_section:
            points = calculate_significant_points(section)
            print(f"Section {i} significant points: {points}")
            for px, py in points:
                if (px, py) not in all_significant_points:
                    all_significant_points.append((px, py))
                    ax.plot(px, py, 'o', color="black", markersize=4, zorder=5)
                    ax.annotate(
                        f"({round(px, 1)}, {round(py, 1)})",
                        xy=(px, py),
                        xytext=(0, 10),
                        textcoords="offset points",
                        fontsize=8,
                        ha="center",
                        color="black",
                        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="white", alpha=0.8)
                    )
