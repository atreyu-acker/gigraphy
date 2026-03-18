import flet as ft
from Backend import database

def login_view(page: ft.Page) -> ft.View:

    # Input fields first
    form_email = ft.TextField(label="Email", width=400)
    form_password = ft.TextField(label="Password", password=True, width=400)
    errorMessage = ft.Text("")  # empty message initially

    # Handler
    def login_handler(e: ft.ControlEvent):
        password = database.get_password(form_email.value)
        if password and form_password.value == password[0]:
            print("Login successful!")
            page.go("/game_home")
        else:
            print("Login failed!")
            errorMessage.value = "Invalid email or password"
            errorMessage.color = "red"
            errorMessage.update()  # important to refresh

    # Buttons
    login_button = ft.ElevatedButton("Login", on_click=login_handler)
    back_button = ft.TextButton("Back", on_click=lambda _: page.go("/"))

    # Header
    header = ft.Text("Login", size=26, weight=ft.FontWeight.BOLD)

    # Return the view
    return ft.View(
        route="/login",
        controls=[
            header,
            form_email,
            form_password,
            login_button,
            errorMessage,
            back_button,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )
