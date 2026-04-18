import flet as ft
from Backend.database import update_password


def reset_password(page):
    password_field = ft.TextField(label="Password", password=True, width=400)
    confirm_field = ft.TextField(label="Confirm Password", password=True, width=400)
    message = ft.Text()

    def handle_reset(_):
        password = password_field.value
        confirm_password = confirm_field.value
        userID = page.session.get("userID")

        success, result = update_password(password, confirm_password, userID) 

        if success:
            page.go("/login")
            
        else:
            if result == "email_exists":
                message.value = "Email already exists"
            elif result == "username_exists":
                message.value = "Username already exists"
            elif result == "password_mismatch":
                message.value = "Passwords do not match"
            elif result == "password_too_short":
                message.value = "Password must be at least 8 characters"
            elif result == "password_no_number":
                message.value = "Password must contain at least one number"
            elif result == "security_info_missing":
                message.value = "Please provide security question info"
            else:
                message.value = "Unknown error"
            message.color = "red"
            message.update()
            
            message.update()

    page.update()



    return ft.View(
        route="/reset_password",
        controls=[
            password_field,
            confirm_field,
            message,
            ft.ElevatedButton("Password Reset", on_click=handle_reset),
            ft.ElevatedButton("Go back", on_click=lambda _:page.go("/login"))
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )