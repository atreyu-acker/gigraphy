import flet as ft
import bcrypt
from Backend import database

def login_view(page: ft.Page) -> ft.View:
    page.title = "Gigraphy Login Screen"

    form_email = ft.TextField(label="Email", width=400)
    form_password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=400)
    errorMessage1 = ft.Text("")
    errorMessage2 = ft.Text("", visible=False)
    forgot_password = ft.TextButton("Forgot Password?", on_click=lambda _: forgot_password_handler())
    security_answer_field = ft.TextField(label="Security Answer", visible=False, width=400)
    security_question_field = ft.TextField(label="", visible=False, width=400)
    reset_password_button = ft.ElevatedButton("Reset Password", visible=False, on_click=lambda _: reset_password_handler())
    
    def forgot_password_handler():
        while form_email.value == "":
            errorMessage1.value = "Please enter your email to reset password"
            errorMessage1.color = "red"
            errorMessage1.update()
            return
        while not database.get_user(form_email.value):
            errorMessage1.value = "Email not found, go back and sign up to create an account"
            errorMessage1.color = "red"
            errorMessage1.update()
            return
        
        errorMessage1.value = ""
        page.update()
        
        security_question_field.visible = True
        security_answer_field.visible = True
        reset_password_button.visible = True
        user = database.get_user(form_email.value)
        security_question = ft.Text(f"Security Question: {user[4]}")
        security_question_field.value = security_question.value
        page.session.set("userID", user[0])
        page.update() 


       
    def reset_password_handler():
        user = database.get_user(form_email.value)
        security_answer = user[5]
        errorMessage2.visible = True
        if security_answer_field.value.lower().strip() == security_answer:
            errorMessage2.value = f"Your password is: {user[2]}"
            errorMessage2.color = "green"
            page.go("/reset_password")
        else:
            errorMessage2.value = "Incorrect security answer"
            errorMessage2.color = "red"
        errorMessage2.update()


    def login_handler(e: ft.ControlEvent):
        user = database.get_user(form_email.value)
        if user and bcrypt.checkpw(form_password.value.encode(), user[2].encode()):
            page.session.set("username", user[3])
            page.session.set("XP", user[6])
            page.go("/game_home")
        else:
            errorMessage1.value = "Invalid email or password"
            errorMessage1.color = "red"
            errorMessage1.update() 


    login_button = ft.ElevatedButton("Login", on_click=login_handler)
    back_button = ft.TextButton("Back to sign up", on_click=lambda _: page.go("/"))


    header = ft.Text("Login", size=26, weight=ft.FontWeight.BOLD)


    return ft.View(
        route="/login",
        controls=[
            header,
            form_email,
            form_password,
            login_button,
            errorMessage1,
            forgot_password,
            security_question_field,
            security_answer_field,
            errorMessage2,
            reset_password_button,
            back_button,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )
