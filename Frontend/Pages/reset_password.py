import flet as ft
from Backend.database import update_password


def reset_password(page):
    password_field = ft.TextField(label="Password", password=True, width=400)
    confirm_field = ft.TextField(label="Confirm Password", password=True, width=400)
    message = ft.Text()

    def handle_reset(e):
        password = password_field.value
        confirm_password = confirm_field.value
        userID = page.session.get("userID")

        if password == confirm_password:
            update_password(password, userID)
            message.value = "Password reset successful"
            message.color = "green"
        else:
            message.value = "Passwords do not match"
            message.color = "red"
        
        message.update()

    page.update()



    return ft.View(
        route="/reset_password",
        controls=[
            password_field,
            confirm_field,
            message,
            ft.ElevatedButton("Password Reset", on_click=handle_reset),
            ft.ElevatedButton("Login", on_click=lambda _: page.go("/login")),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )