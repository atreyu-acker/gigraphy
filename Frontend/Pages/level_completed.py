import flet as ft
from Backend.database import add_XP
from Backend.database import add_history


def level_completed(page):
    difficulty = page.session.get("difficulty")
    userID = page.session.get("userID")

    XP_dictionary = {
        "Beginner": 10,
        "Easy": 20,
        "Medium": 40,
        "Hard": 60,
        "Expert": 90
    }   

    XP_gain = XP_dictionary[difficulty]

    add_XP(page.session.get("username"), XP_gain)
    add_history(userID, difficulty, True, XP_gain)
    
    return ft.View(
        route="/level_completed",
        controls=[
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=24,
                controls=[
                    ft.Text(f"Well done {page.session.get('username')}, Level Complete!", size=32, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Difficulty: {difficulty}", size=18),
                    ft.Text(f"Score + {XP_dictionary[difficulty]}", size=24, weight=ft.FontWeight.BOLD),
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