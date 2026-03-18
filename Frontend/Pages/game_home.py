import flet as ft

def game_home(page: ft.Page) -> ft.View:
    page.title = "Game Home Screen"
    page.padding = 20

    username = "Player1"
    xp = 1500

    top_bar = ft.Row(
        background_color=ft.Colors.BLUE_500,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(
                spacing=10,
                controls=[
                    ft.Text(f"{username}", size=20, color="white"),
                    ft.Text(f"XP: {xp}", size=20, weight="bold", color="gold")
                ]
            ),
            ft.ElevatedButton("⚙️ Settings")
        ]
    )


    middle_section = ft.Column(
        background_color=ft.Colors.BROWN_200,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        controls=[
            ft.ElevatedButton(
                "Choose Difficulty / Level",
                width=200,
                height=50
            ),
            ft.ElevatedButton(
                "Start Game / Level",
                width=200,
                height=60
            )
        ]
    )


    bottom_bar = ft.Row(
        background_color=ft.Colors.BROWN_100,
        alignment=ft.MainAxisAlignment.START,
        controls=[
            ft.ElevatedButton("Leaderboard")
        ]
    )


    return ft.View(
        route="/game_home",
        controls=[
            ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    top_bar,
                    middle_section,
                    bottom_bar
                ]
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )   

    