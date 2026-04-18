import flet as ft
import bcrypt  # this is used to hash later.
from Backend import database

def login_view(page):  # returns a view.
    page.title = "Gigraphy Login Screen"

    # these are the definitions for the controls which are returned at the end.
    form_email = ft.TextField(label="Email", width=400)
    form_password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=400)   # here can_reveal_password is what allows the password to be private or viasable.
    errorMessage1 = ft.Text("")  
    errorMessage2 = ft.Text("", visible=False)   # this error message is for the forgot password section and is only set to viasable=True when that happens.
    forgot_password = ft.TextButton("Forgot Password?", on_click=lambda _: forgot_password_handler())   # sends the user to forgot_password_handler when clicked.
    security_answer_field = ft.TextField(label="Security Answer", visible=False, width=400)
    security_question_field = ft.TextField(label="", visible=False, width=400)
    reset_password_button = ft.ElevatedButton("Reset Password", visible=False, on_click=lambda _: reset_password_handler())
    login_button = ft.ElevatedButton("Login", on_click=lambda _: login_handler())
    back_button = ft.TextButton("Back to sign up", on_click=lambda _: page.go("/"))
    header = ft.Text("Login", size=26, weight=ft.FontWeight.BOLD)


    # this function is called when forgot password is clicked.
    def forgot_password_handler():  # the function passes a _ so python does not care that its not used its just there because it is a handler and has an event.
        # here the email of the user is needed for the next query to the database. 
        while form_email.value == "":
            errorMessage1.value = "Please enter your email to reset password"
            errorMessage1.color = "red"
            errorMessage1.update()
            return
        user = database.get_user(form_email.value.strip().lower())    # user is now holding a list of 7 values because get_user gets every value from a user row. 
        page.session.set("user", user)    # page.session allows a variable to be set to page and can be accessed at other points as it is passed by page in every function. it is only temporary.

        while user is None:   # checks if the user actually exists.
            errorMessage1.value = "Email not found, go back and sign up to create an account"
            errorMessage1.color = "red"
            errorMessage1.update()
            return
        
        errorMessage1.value = ""
        page.update()   # important so the page changes emidiatly to show the message. 

        # this only happens if emial is there and valid.
        security_question_field.visible = True   # I initially set these to be invisable so they only appear when forgot password is clicked.
        security_answer_field.visible = True  
        reset_password_button.visible = True 
        security_question = ft.Text(f"Security Question: {user[4]}")   # user at position 4 is the security question.
        security_question_field.value = security_question.value   
        page.update() 


    # this function is called when they click reset password after entering the security question, it checks if they can continue.
    def reset_password_handler():
        user = page.session.get("user")  
        security_answer = user[5]  # retrieves the correct answer of the security question.
        errorMessage2.visible = True
        if security_answer_field.value.lower().strip() == security_answer:  # compares the input to the answer (.lower() and .strip() eliminate errors with capitals and spaces).
            page.go("/reset_password")   # when correct can go to reset their password.
        else:
            errorMessage2.value = "Incorrect security answer"
            errorMessage2.color = "red"
        errorMessage2.update()

    # this function occurs when they press login to check if the password and email are correct.
    def login_handler():   
        user = database.get_user(form_email.value.strip().lower()) 
        page.session.set("userID", user[0]) # i am setting a value for the user ID for use in history page later.
        page.session.set("user", user)
        if user is not None and bcrypt.checkpw(form_password.value.encode(), user[2].encode()):  # uses bcrypt to hash the password before its stored to the database.
            page.session.set("username", user[3])
            page.session.set("XP", user[6])
            page.go("/game_home")
        else:
            errorMessage1.value = "Invalid email or password"  # the error massages if user doesnt exist.
            errorMessage1.color = "red"
            errorMessage1.update() 


    # this is the collection of controls put together to create the view.
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
