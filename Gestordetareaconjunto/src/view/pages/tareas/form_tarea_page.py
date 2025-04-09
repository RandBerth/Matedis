import flet as ft
from model.tarea_model import Tarea

class FormTareaPage(ft.Column):
    def __init__(self, page: ft.Page, tarea=None, on_save=None):
        super().__init__()
        self.page = page
        self.tarea = tarea
        self.on_save = on_save

        self.nombre = ft.TextField(label="Nombre", value=tarea.nombre if tarea else "")
        self.descripcion = ft.TextField(label="Descripción", multiline=True, value=tarea.descripcion if tarea else "")
        self.tipo = ft.Dropdown(
            label="Tipo",
            options=[
                ft.dropdown.Option("clase"),
                ft.dropdown.Option("comida"),
                ft.dropdown.Option("rutina"),
                ft.dropdown.Option("recordatorio"),
                ft.dropdown.Option("otro")
            ],
            value=tarea.tipo if tarea else "otro"
        )
        self.color = ft.TextField(label="Color", value=tarea.color if tarea else "#FFFF00")

        self.controls = [
            self.nombre,
            self.descripcion,
            self.tipo,
            self.color,
            ft.Row([
                ft.ElevatedButton("Cancelar", on_click=self.cancelar),
                ft.ElevatedButton("Guardar", on_click=self.guardar)
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
        ]

    def cancelar(self, e):
        self.page.dialog.open = False
        self.page.update()

    def guardar(self, e):
        if not self.nombre.value or not self.tipo.value:
            self.page.snack_bar = ft.SnackBar(ft.Text("Por favor, llena los campos obligatorios"), open=True)
            self.page.update()
            return

        db = self.page.database
        nueva = Tarea(
            id=self.tarea.id if self.tarea else None,
            nombre=self.nombre.value,
            descripcion=self.descripcion.value,
            tipo=self.tipo.value,
            color=self.color.value,
        )

        if self.tarea:
            Tarea.update(db, nueva)
        else:
            Tarea.insert(db, nueva)

        if self.on_save:
            self.on_save()
