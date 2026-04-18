import flet as ft
import Backend.database    # this allows this file to use functions in the database file.


# honestly not sure when to write it in a fancy way and when to just put page, it is the same but more proffesional like this. 
# it is telling python and the user that page returns a view. i only use it in this file.
def signup_view(page: ft.Page) -> ft.View:   
    page.title = "Gigraphy Signup Screen"

# these are the definitions for the controls which i can now just list at the end.
    username_field = ft.TextField(label="Username", width=400)
    email_field = ft.TextField(label="Email", width=400)
    password_field = ft.TextField(label="Password", can_reveal_password=True, password=True, width=400)
    confirm_field = ft.TextField(label="Confirm Password", can_reveal_password=True, password=True, width=400)
    security_answer_field = ft.TextField(label="Security Question", width=400)
    message = ft.Text("")

    # the list of security questions for the user.
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

   # builds the dropdown menu whith the question options.
    security_question_dropdown = ft.Dropdown(
        label="Select a security question",
        width=400,
        options=[ft.dropdown.Option(question) for question in security_questions]
    )

    # this is called when the user clicks create account and e is an event.
    def handle_signup(_):
        # here i call a function in the database file which creates the user by adding their details to the dtabase with the listed values.
        success, result = Backend.database.create_user(
            email_field.value,
            password_field.value,
            confirm_field.value,
            username_field.value,
            security_question_dropdown.value,
            security_answer_field.value
        )

        # create_user returns a tupple, if the account was successful and the message
        # this is the success path if all the inputs are valid.
        if success:
            message.value = "Account created"
            message.color = "green"
            message.update()
            page.session.set("username", username_field.value)
            page.session.set("xp", 0)
            page.go("/game_home")
            return

        # this is the not success path which checks what error message should be displayed.
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

    # the page is returned/ displayed.
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
            ft.ElevatedButton("Create Account", on_click=handle_signup),  # when this button is clicked go to handle_signup.
            message,
            ft.TextButton("Back to login", on_click=lambda _: page.go("/")),  # when this is clicked go to "/" which is the welcome page.
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,

    )