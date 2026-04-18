import flet as ft           # this is a fundemental part of my code, importing flet library is what allows me to build pages using flets UI controls.

# in small pages like this it is easy to define and build controls directly into the return of the function, however, for larger pages i define many controls earlier (see login)
def welcome_view(page):     # the function that creates and returns the page view.
    return ft.View(         # this line returns the view/page. 
        route="/",          # route= tells main.py where the page is for page.go its like the path for the computer to follow.
        controls=[          # the controls is what actually builds the page.
            
            # this is the tesxt at the top of the page.
            ft.Text("Welcome to Gigraphy", size=30, weight=ft.FontWeight.BOLD),           
            # using flets inbuilt ElevatedButton that the user can click on to go to login.
            ft.ElevatedButton("Login", height=50, width=160, style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)), on_click=lambda _: page.go("/login")),    
            ft.ElevatedButton("Sign Up", height=50, width=160, style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)), on_click=lambda _: page.go("/signup")),      
        ],      # ButonStyle allows me to manualy edit the size of the button which i wanted larger than the default.

        horizontal_alignment=ft.CrossAxisAlignment.CENTER,     # this tells flet which alignment the page is using, basically that everything should be in the center
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )