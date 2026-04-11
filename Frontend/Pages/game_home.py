import flet as ft
from Backend.database import get_XP

def game_home(page: ft.Page) -> ft.View:
    page.title = "Gigraphy Home Screen"

    username = page.session.get("username")
    XP = get_XP(username)
    page.session.set("XP", XP)

    difficulty_dropdown = ft.Dropdown(
    label="Difficulty",
    width=200,
    options=[
        ft.dropdown.Option("Beginner"),
        ft.dropdown.Option("Easy"),
        ft.dropdown.Option("Medium"),
        ft.dropdown.Option("Hard"),
        ft.dropdown.Option("Expert"),
    ]
    )


    error = ft.Text("")

    def start_game(e):
        if not difficulty_dropdown.value:
            error.value = "Please select a difficulty and level"
            error.color = "red"
            error.update()
            return
        page.session.set("difficulty", difficulty_dropdown.value)
        page.go("/game_play")

    def logout(e):
        page.session.clear()
        page.go("/")

    top_bar = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(f"      Welcome {username}", size=25),
            ft.Text(f'XP: {XP}', size=25, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton("Log out", on_click=logout)
        ]
    )


    middle_section = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        controls=[
            ft.Text("Select your level", size=22, weight=ft.FontWeight.BOLD),
            difficulty_dropdown,
            ft.ElevatedButton(
                content=ft.Text("Start Game", size=18),
                on_click=start_game,
                width=250
            ),
            error
        ]
    )

    bottom_bar = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.ElevatedButton(
                content=ft.Text("Leaderboard", size=18),
                on_click=lambda _: page.go("/leaderboard"),
                width=250
            )
        ]
    )

    return ft.View(
        route="/game_home",
        controls=[
            ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[top_bar, middle_section, bottom_bar]
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )