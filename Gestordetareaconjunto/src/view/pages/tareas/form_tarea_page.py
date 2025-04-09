import flet as ft
from model.tarea_model import Tarea, insert_tarea
from model.db_config import get_db_connection

class FormTareaPage(ft.Column):
    def __init__(self, page: ft.Page, tarea=None, on_save=None):
        super().__init__()
        self.page = page
        self.db_connection = get_db_connection()  # Obtener conexión aquí
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

        try:
            # Crear objeto Tarea
            nueva = Tarea(
                id=self.tarea.id if self.tarea else None,
                nombre=self.nombre.value,
                descripcion=self.descripcion.value,
                tipo=self.tipo.value,
                color=self.color.value,
            )

            # Verificar que la conexión esté activa
            if self.db_connection is None:
                self.db_connection = get_db_connection()

            # Guardar en la base de datos
            if self.tarea and self.tarea.id:
                from model.tarea_model import update_tarea
                update_tarea(self.db_connection, nueva)
            else:
                insert_tarea(self.db_connection, nueva)

            # Cerrar diálogo y actualizar
            self.page.dialog.open = False
            self.page.update()

            # Llamar al callback si existe
            if self.on_save:
                self.on_save()
                
        except Exception as ex:
            print(f"Error al guardar tarea: {ex}")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"), open=True)
            self.page.update()
        finally:
            # Cerrar la conexión
            if self.db_connection:
                self.db_connection.close()