import flet as ft
from Backend.database import add_XP, get_XP 

def level_completed(page: ft.Page) -> ft.View:
    difficulty = page.session.get("difficulty")

    XP_dictionary = {
        "Beginner": 10,
        "Easy": 20,
        "Medium": 30,
        "Hard": 40,
        "Expert": 50
    }   

    add_XP(page.session.get("username"), XP_dictionary[difficulty])

    
    return ft.View(
        route="/level_completed",
        controls=[
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=24,
                controls=[
                    ft.Text(f"Well done {page.session.get('username')} Level Complete!", size=32, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Difficulty: {difficulty}", size=18),
                    ft.Text(f"Score + : {XP_dictionary[difficulty]}", size=24, weight=ft.FontWeight.BOLD),
                    ft.ElevatedButton(
                        "Continue",
                        width=200,
                        on_click=lambda _: page.go("/game_home")
                    ),
                ]
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )