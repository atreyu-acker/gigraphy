import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib
matplotlib.use("Agg")
from Algorithms.graph_alg import generate_level, difficulty_map
from Algorithms.checker_alg import check_coefficients
from Frontend.draw_graphs import draw_sections
from Backend.database import add_XP, get_XP

def game_play(page: ft.Page) -> ft.View:
    page.title = "Gigraphy Play Screen"

    difficulty = page.session.get("difficulty") or "Beginner"
    sections = generate_level(difficulty)
    num_sections = len(sections)
    current_section = [0]


    # equation form labels per type
    equation_formula = {
        "linear": "y = mx + c",
        "quadratic": "y = ax² + bx + c"
    }

    # build initial chart
    fig = draw_sections(sections, 0)
    chart_container = ft.Container(
        content=MatplotlibChart(figure=fig, expand=True),
        expand=True,
        height=400,
    )

    feedback = ft.Text("", size=16)
    section_text = ft.Text(f"Equation 1 of {num_sections}", size=16)
    score_text = ft.Text(f"Score: {get_XP(page.session.get('username'))}", size=16, weight=ft.FontWeight.BOLD)

   
    eq_formula_field = ft.Text(
    equation_formula[sections[0]["equation_type"]],
    size=20,
    italic=True
    )

    input_container = ft.Row(
    alignment=ft.MainAxisAlignment.CENTER,
    spacing=16
    )

    def build_input_fields():
        
        current_keys = list(sections[current_section[0]]["coefficients"].keys())

        eq_type = sections[current_section[0]]["equation_type"]
        eq_formula_field.value = equation_formula[eq_type]
        input_fields.clear()
        input_container.controls.clear()
        if eq_formula_field.page:
            eq_formula_field.update()
        for key in current_keys:
            field = ft.TextField(
                label=key,
                width=120,
                keyboard_type=ft.KeyboardType.NUMBER
            )
            input_fields[key] = field
            input_container.controls.append(field)
        if input_container.page:
            input_container.update()  

    input_fields = {}
    build_input_fields()

    def check_answer(e):
        user_inputs = {key: field.value for key, field in input_fields.items()}
        correct = sections[current_section[0]]["coefficients"]
        print(correct)
        all_correct, results = check_coefficients(user_inputs, correct)

        for key, result in results.items():
            field = input_fields[key]
            if result == "correct":
                field.border_color = "green"
            elif result == "incorrect":
                field.border_color = "red"
            elif result == "invalid":
                field.border_color = "red"
                feedback.value = f"Please enter a valid number for {key}"
                feedback.color = "red"
                feedback.update()
                return
            field.update()

        if all_correct:

            if current_section[0] < len(sections) - 1:
                current_section[0] += 1
                section_text.value = f"Equation {current_section[0] + 1} of {num_sections}"
                section_text.update()
                feedback.value = f"Correct! Now find equation {current_section[0] + 1}"
                feedback.color = "green"
                build_input_fields()
                input_container.update()

                # redraw with new active section
                new_fig = draw_sections(sections, current_section[0])
                chart_container.content = MatplotlibChart(figure=new_fig, expand=True)
                chart_container.update()

            else:
                feedback.value = "Level complete!"
                feedback.color = "green"
                page.go("/level_completed")
        else:
            feedback.value = "Not quite — check the highlighted fields"
            feedback.color = "red"

        feedback.update()

    def quit_level(e):
        page.go("/game_home")

    top_bar = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(f"Difficulty: {difficulty}", size=15),
            section_text,
            score_text,
            ft.ElevatedButton("Quit level", on_click=quit_level)
        ]
    )

    input_section = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
        controls=[
            ft.Text("Find the equation:", size=15),
            eq_formula_field,
            input_container,
            ft.ElevatedButton("Submit Answer", on_click=check_answer),
            feedback,
        ]
    )

    return ft.View(
        route="/game_play",
        controls=[
            ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    top_bar,
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        controls=[chart_container, input_section]
                    )
                ]
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.START,
        scroll=ft.ScrollMode.AUTO
    )

