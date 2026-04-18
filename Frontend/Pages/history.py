import flet as ft
from Backend.database import get_history


def history(page):
    page.title = "Game History"
    userID = page.session.get("userID")
    username = page.session.get("username")
    title_text = ft.Text(f"{username}'s Level History", size=30, weight=ft.FontWeight.BOLD)

    # this can be changed, i think 20 past levels is enough, its just a proof of concept i could later add a load more history part.
    limit = 30

    rows = []

    history_row = get_history(userID, limit) # returns a list

    if history_row != []: # checks the list is not empty
        for level_difficulty, completed, date, XP_gained in history_row:
            if completed:
                success = "completed"
            else:
                success = "quit"

            if level_difficulty[0] == "E":
                indef_article = "an"
            else:
                indef_article = "a"

            rows.append(
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    controls=[
                        ft.Text(f"You {success} {indef_article} {level_difficulty.lower()} level on {date} and gained {XP_gained} XP", size=18)
                    ]
                )
            )
    else:
        rows = [ft.Row(
                    controls=[
                        ft.Text("You have no history, go and start a level", size=20, color="red")
                    ]
                )]
    


    return ft.View(
    route="/history",
    controls=[
        ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            controls=[
                ft.Column(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[title_text]
                        )
                    ]
                ),

                ft.Divider(),

                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[                       
                        ft.Container(
                            width=400,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                controls=rows
                            )
                        )
                    ]
                ),

                ft.Divider(),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[                       
                        ft.ElevatedButton(
                            "Back to Game Home",
                            on_click=lambda e: page.go("/game_home")
                        )
                    ]
                ),
            ]
        )
    ],
    vertical_alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER
)