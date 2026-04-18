import flet as ft
from Backend.database import get_leaderboard


def leaderboard(page):
    page.title = "Leaderboard"
    data = get_leaderboard(30)
    rows = []
    leaderboard_text = ft.Text("Leaderboard", size=30, weight=ft.FontWeight.BOLD)

    for i, (username, xp) in enumerate(data, start=1):
        rows.append(
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(f"{i}.", width=40),
                    ft.Text(username, expand=True),
                    ft.Text(f"{xp} XP", weight=ft.FontWeight.BOLD)
                ]
            )
        )

    return ft.View(
        route="/leaderboard",
        controls=[
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    leaderboard_text,
                    ft.Divider(),
                    ft.Column(
                        width=400,
                        controls=rows
                    ),
                    ft.ElevatedButton(
                        "Back to Game Home",
                        on_click=lambda e: page.go("/game_home")
                    )
                ]
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )