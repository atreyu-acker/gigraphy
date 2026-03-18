import flet as ft
from Frontend.Pages.welcome import welcome_view
from Frontend.Pages.login import login_view
from Frontend.Pages.signup import signup_view
from Frontend.Pages.game_home import game_home
from Frontend.Pages.game_play import game_play

def main(page: ft.Page) -> None:
    page.title = "Gigraphy"
    page.theme_mode = ft.ThemeMode.LIGHT    
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER


    view_factories = {
        "/": welcome_view,
        "/login": login_view,
        "/signup": signup_view,
        "/game_home": game_home,
        "/game_play": game_play,
    }

    def route_change(route):
        page.views.clear()
        factory = view_factories.get(page.route, welcome_view)
        view = factory(page)  
        page.views.append(view)
        page.update()

    page.on_route_change = route_change

    page.go("/")

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)