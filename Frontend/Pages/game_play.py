import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from Algorithms.graph_alg import generate_level, draw_sections
from Algorithms.checker_alg import check_coefficients



def game_play(page: ft.Page) -> ft.View:
    page.title = "Gigraphy Play Screen"

    difficulty = page.session.get("difficulty")
    NUM_SECTIONS = 5
    
    current_section = [0]

    fig, ax = plt.subplots(figsize=(14, 5))
    sections = generate_level(difficulty)
    draw_sections(ax, sections, current_section[0])

    
    print(current_section)

    feedback = ft.Text("", size=16)
    section_text = ft.Text(f"Equation 1 of {NUM_SECTIONS}", size=16)

    input_container = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=16
    )

    def build_input_fields():
        current_keys = list(sections[current_section[0]]["coefficients"].keys())
        input_fields.clear()
        input_container.controls.clear()
        for key in current_keys:
            field = ft.TextField(
                label=key,
                width=120,
                keyboard_type=ft.KeyboardType.NUMBER
            )
            input_fields[key] = field
            input_container.controls.append(field)
        

    input_fields = {}
    build_input_fields()

    XP_dictionary = {
        "Beginner": 10,
        "Easy": 20,
        "Medium": 30,
        "Hard": 40,
        "Expert": 50
    }   

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
                section_text.value = f"Equation {current_section[0] + 1} of {NUM_SECTIONS}"
                section_text.update()
                feedback.value = f"Correct! Now find equation {current_section[0] + 1}"
                feedback.color = "green"
                build_input_fields()
                input_container.update()

                # redraw graph with new active section
                ax.cla()
                draw_sections(ax, sections, current_section[0])
                chart_container.content = MatplotlibChart(figure=fig, expand=True)
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

   
    draw_sections(ax, sections)

    

    chart_container = ft.Container(
        content=MatplotlibChart(figure=fig, expand=True),
        expand=True, 
    )

    top_bar = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(f"Difficulty: {difficulty}", size=15),
            section_text,
            ft.ElevatedButton("Quit level", on_click=quit_level)
        ]
    )

  
    input_section = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
        controls=[
            ft.Text("Find the equation:", size=15),
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