import flet as ft
# Corregir las importaciones para que funcionen correctamente
from src.view.pages.tareas.tareas import TareasPage
from src.view.pages.encargados.encargados import EncargadosPage
from src.view.pages.conjuntos.conjuntos import ConjuntosPage

def main(page: ft.Page):
    page.title = "Gestor de Tareas"
    page.theme_mode = "light"
    page.scroll = "auto"

    # Añadir mensaje de depuración
    print("Iniciando aplicación Flet - Gestor de Tareas")

    content_area = ft.Container(expand=True)

    def change_view(index):
        print(f"Cambiando a la vista {index}")
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
                    # Actualizar a la nueva sintaxis de iconos
                    icon=ft.icons.TASK_OUTLINED, 
                    selected_icon=ft.icons.TASK,
                    label="Tareas"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.PEOPLE_OUTLINED,
                    selected_icon=ft.icons.PEOPLE,
                    label="Encargados"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.GRID_VIEW_OUTLINED,
                    selected_icon=ft.icons.GRID_VIEW,
                    label="Conjuntos"
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
    print("Interfaz inicializada correctamente")

# ESTA PARTE ES CRUCIAL
if __name__ == "__main__":
    print("Iniciando aplicación Flet...")
    try:
        # Intenta ejecutar como aplicación web
        ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550)
    except Exception as e:
        print(f"Error al ejecutar como aplicación web: {e}")
        try:
            # Si falla, intenta como aplicación de escritorio
            ft.app(target=main, view=ft.AppView.FLET_APP)
        except Exception as e:
            print(f"Error al ejecutar como aplicación de escritorio: {e}")
            # Último intento con configuración mínima
            ft.app(target=main)