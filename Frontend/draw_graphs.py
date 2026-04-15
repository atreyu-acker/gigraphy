import matplotlib
matplotlib.use("Agg")
import numpy as np
from Algorithms.graph_alg import calculate_significant_points
from Algorithms.graph_alg import extend_linear, extend_quadratic


def draw_sections(ax, sections, active_section=0):
    x_range_end = len(sections) * 25 + 10
    ax.set_xlim(0, x_range_end)

    colors = ["steelblue", "orange", "green", "red", "purple"]

    all_y = []
    for i, section in enumerate(sections):
        if section["equation_type"] == "linear":
            all_y.extend([section["y_start"], section["y_end"]])
        else:
            all_y.extend(section["y_values"].tolist())

    y_min = min(-20, min(all_y) - 10)
    y_max = max(70, max(all_y) + 10)

    ax.set_ylim(y_min, y_max)
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("x", fontsize=10)
    ax.set_ylabel("y", fontsize=10, rotation=0)

    active_x_start = sections[active_section]["x_start"]
    ax.axvline(active_x_start, color="black", linewidth=0.8)

    tick_step = 5
    x_min, x_max = ax.get_xlim()
    first_tick = tick_step * int(np.floor(x_min / tick_step))
    xticks = np.arange(first_tick, x_max + tick_step, tick_step)
    ax.set_xticks(xticks)
    ax.set_xticklabels(
        [
            str(int(round(t - active_x_start, 1)))
            if round(t - active_x_start, 1) == int(round(t - active_x_start, 1))
            else str(round(t - active_x_start, 1))
            for t in xticks
        ]
    )

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
            if i == active_section:
                if section["x_start"] > 0:
                    extend_linear(ax, m, c, 0, section["x_start"], section["x_start"], color)
                if section["x_end"] < x_range_end:
                    extend_linear(ax, m, c, section["x_end"], x_range_end, section["x_start"], color)

        elif section["equation_type"] == "quadratic":
            a = section["coefficients"]["a"]
            b = section["coefficients"]["b"]
            c = section["coefficients"]["c"]

            ax.plot(
                section["x_values"],
                section["y_values"],
                color=color,
                linewidth=2
            )
            if i == active_section:
                if section["x_start"] > 0:
                    extend_quadratic(ax, a, b, c, 0, section["x_start"], section["x_start"], color)
                if section["x_end"] < x_range_end:
                    extend_quadratic(ax, a, b, c, section["x_end"], x_range_end, section["x_start"], color)

        
        if i == active_section:
            raw_points = calculate_significant_points(section)
            seen = set()
            points = []
            for px, py in raw_points:
                point_key = (round(px, 6), round(py, 6))
                if point_key in seen:
                    continue
                seen.add(point_key)
                points.append((px, py))

            placed_points = []
            text_offsets = [
                (0, 14),
                (0, -22),
                (18, 16),
                (-18, 16),
                (22, -20),
                (-22, -20),
                (30, 10),
                (-30, 10),
            ]
            for px, py in points:
                ax.plot(px, py, 'o', color="black", markersize=4, zorder=5)
                close_count = sum(
                    1
                    for ox, oy in placed_points
                    if abs(px - ox) <= 3 and abs(py - oy) <= 3
                )
                placed_points.append((px, py))
                offset_x, offset_y = text_offsets[close_count % len(text_offsets)]
                local_x = px - active_x_start
                ax.annotate(
                    f"({int(round(local_x, 1)) if round(local_x, 1) == int(round(local_x, 1)) else round(local_x, 1)}, "
                    f"{int(round(py, 1)) if round(py, 1) == int(round(py, 1)) else round(py, 1)})",
                    xy=(px, py),
                    xytext=(offset_x, offset_y),
                    textcoords="offset points",
                    fontsize=8,
                    ha="center",
                    color="black",
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="white", alpha=0.8)
                )
