import flet as ft
import Backend.database

def signup_view(page: ft.Page) -> ft.View:
    page.title = "Gigraphy Signup Screen"


    username_field = ft.TextField(label="Username", width=400)
    email_field = ft.TextField(label="Email", width=400)
    password_field = ft.TextField(label="Password", can_reveal_password=True, password=True, width=400)
    confirm_field = ft.TextField(label="Confirm Password", can_reveal_password=True, password=True, width=400)
    security_answer_field = ft.TextField(label="Security Question", width=400)
    message = ft.Text("")

    security_questions = [
        "What is your mother's maiden name?",
        "What was the name of your first pet?",
        "What was the make of your first car?",
        "In what city were you born?",
        "What is your favorite book?",
        "What is your favorite movie?",
        "What is your favorite food?",
        "What is the name of the street you grew up on?"
    ]   
    
    security_question_dropdown = ft.Dropdown(
        label="Select a security question",
        width=400,
        options=[ft.dropdown.Option(question) for question in security_questions]
    )

    def handle_signup(e):
        success, result = Backend.database.create_user(
            email_field.value,
            password_field.value,
            confirm_field.value,
            username_field.value,
            security_question_dropdown.value,
            security_answer_field.value
        )

        if success:
            message.value = "Account created"
            message.color = "green"
            message.update()
            page.session.set("username", username_field.value)
            page.session.set("xp", 0)
            page.go("/game_home")
            return


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

    return ft.View(
        route="/signup",
        controls=[
            ft.Text("Create Account", size=26),
            username_field,
            email_field,
            password_field,
            confirm_field,
            security_question_dropdown,
            security_answer_field,
            ft.ElevatedButton("Create Account", on_click=handle_signup),
            message,
            ft.TextButton("Back to login", on_click=lambda _: page.go("/")),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )
