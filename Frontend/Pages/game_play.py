import flet as ft
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg") 

def game_play(page: ft.Page) -> ft.View:
    page.title = "MatplotlibChart Example"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # 1. Create a Matplotlib figure and axes
    fig, ax = plt.subplots()
    
    # 2. Plot data on the axes
    x_values = [1, 2, 3, 4]
    y_values = [10, 20, 25, 30]
    ax.plot(x_values, y_values, marker="o")
    
    # 3. Set plot properties (optional)
    ax.set_title("Simple Line Plot")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")

    # 4. Create the Flet MatplotlibChart control and add it to the page
    # `expand=True` makes the chart fill the available space
    chart_control = ft.Container(content=MatplotlibChart(figure=fig), width=600, height=400)

    # Game play content
    game_content = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        controls=[
            chart_control,
            ft.ElevatedButton("End Game", width=150, height=50)
        ]
    )

    return ft.View(
        route="/game_play",
        controls=[game_content],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )