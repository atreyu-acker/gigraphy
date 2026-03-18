import flet as ft
import Backend.database
from Frontend.Pages.game_home import game_home

def signup_view(page: ft.Page) -> ft.View:

    username_field = ft.TextField(label="Username", width=400)
    email_field = ft.TextField(label="Email", width=400)
    password_field = ft.TextField(label="Password", password=True, width=400)
    confirm_field = ft.TextField(label="Confirm Password", password=True, width=400)
    message = ft.Text("")

    def handle_signup(e):
        success, result = Backend.database.create_user(
            email_field.value,
            password_field.value,
            confirm_field.value,
            username_field.value
        )

        if success:
            message.value = "Account created"
            message.color = "green"
            message.update()
            page.go("/game_home")
            return


        if result == "email_exists":
            message.value = "Email already exists"
        elif result == "username_exists":
            message.value = "Username already exists"
        elif result == "password_mismatch":
            message.value = "Passwords do not match"
        else:
            message.value = "Unknown error"

        message.color = "red"
        message.update()

    return ft.View(
        route="/signup",
        controls=[
            ft.Text("Create Account", size=26),
            username_field,
            email_field,
            password_field,
            confirm_field,
            ft.ElevatedButton("Create Account", on_click=handle_signup),
            message,
            ft.TextButton("Back", on_click=lambda _: page.go("/")),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )
