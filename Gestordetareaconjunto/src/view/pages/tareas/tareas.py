import flet as ft 
from controller.tarea_controller import obtener_tareas, eliminar_tarea
from view.pages.tareas.form_tarea_page import FormTareaPage

def TareasPage(page: ft.Page):
    lista = ft.Column(expand=True, spacing=10)

    # Crear diálogo una sola vez
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(""),
        content=ft.Text(""),
        actions=[],
        open=False
    )
    page.dialog = dialog
    page.overlay.append(dialog)  # Necesario para que el diálogo funcione

    def cargar_tareas():
        tareas = obtener_tareas()
        lista.controls.clear()
        if not tareas:
            lista.controls.append(ft.Text("No hay tareas disponibles"))
        else:
            for tarea in tareas:
                lista.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Container(width=10, height=10, bgcolor=tarea.color, border_radius=50),
                            ft.Column([
                                ft.Text(tarea.nombre, weight="bold"),
                                ft.Text(tarea.descripcion or "Sin descripción", size=12)
                            ], expand=True),
                            ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, t=tarea: abrir_formulario(t)),
                            ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, t=tarea: eliminar(e, t.id))
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=10,
                        border=ft.border.all(1, ft.colors.GREY),
                        border_radius=10,
                        margin=5,
                    )
                )
        page.update()

    def abrir_formulario(tarea=None):
        def al_guardar():
            cargar_tareas()
            page.update()

        # Ahora solo pasamos page, tarea y on_save
        contenido_formulario = FormTareaPage(page, tarea, on_save=al_guardar)
        dialog.title = ft.Text("Nueva Tarea" if tarea is None else "Editar Tarea")
        dialog.content = contenido_formulario
        dialog.actions = []  # No acciones adicionales necesarias
        dialog.open = True
        page.update()

    def eliminar(e, tarea_id):
        eliminar_tarea(tarea_id)
        cargar_tareas()

    view = ft.Column([
        ft.Row([
            ft.Text("Tareas", style="titleLarge"),
            ft.IconButton(icon=ft.icons.ADD, on_click=lambda e: abrir_formulario())
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        lista
    ], expand=True)

    cargar_tareas()
    return view