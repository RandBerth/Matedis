import flet as ft
from view.pages.tareas.tareas import TareasPage
from view.pages.encargados.encargados import EncargadosPage
from view.pages.conjuntos.conjuntos import ConjuntosPage

def main(page: ft.Page):
    page.title = "Gestor de Tareas"
    page.theme_mode = "light"
    page.scroll = "auto"

    content_area = ft.Container(expand=True)

    def change_view(index):
        if index == 0:
            content_area.content = TareasPage()
        elif index == 1:
            content_area.content = EncargadosPage()
        elif index == 2:
            content_area.content = ConjuntosPage()
        page.update()

    # Container para NavigationRail con altura definida
    nav_rail_container = ft.Container(
        content=ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.TASK, label="Tareas"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.PEOPLE, label="Encargados"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.GRID_VIEW, label="Conjuntos"
                ),
            ],
            expand=True,
            on_change=lambda e: change_view(e.control.selected_index),
        ),
        height=500,  # Establecer altura para el NavigationRail
        expand=False  # El contenedor no se expandirá, solo el NavigationRail lo hará
    )

    page.add(
        ft.Row(
            [
                nav_rail_container,
                ft.VerticalDivider(width=1),
                content_area
            ],
            expand=True,
        )
    )

    change_view(0)
