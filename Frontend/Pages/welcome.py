import flet as ft

def welcome_view(page):
    return ft.View(
        route="/",
        controls=[
            ft.Text("Welcome to Gigraphy", size=30, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton("Login", height=50, width=160, style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)), on_click=lambda _: page.go("/login")),
            ft.ElevatedButton("Sign Up", height=50, width=160, style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)), on_click=lambda _: page.go("/signup")),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )