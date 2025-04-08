import flet as ft
from model.tarea_model import Tarea

class FormTareaPage:
    def __init__(self, page, tarea=None):
        self.page = page
        self.tarea = tarea
        self._nombre = ft.TextField(label="Nombre", autofocus=True)
        self._descripcion = ft.TextField(label="Descripción", multiline=True)
        self._tipo = ft.Dropdown(
            label="Tipo",
            options=["clase", "comida", "rutina", "recordatorio", "otro"]
        )
        self._color = ft.ColorPicker(label="Color")
        self._fecha_recordatorio = None
        self._hora_inicio = None
        self._hora_fin = None
        self._lugar_id = None
        self._lugares_disponibles = []

    def build(self):
        self._load_lugares()

        return ft.Column(
            [
                self._nombre,
                self._descripcion,
                self._tipo,
                self._color,
                self._get_fecha_recordatorio(),
                self._get_hora_inicio(),
                self._get_hora_fin(),
                self._get_buttons()
            ]
        )

    def _load_lugares(self):
        # Cargar lugares desde la base de datos
        db = self.page.database

    def _get_fecha_recordatorio(self):
        return ft.Row(
            [
                ft.Text("Fecha del recordatorio"),
                ft.ElevatedButton(
                    text="Seleccionar fecha",
                    on_click=self._seleccionar_fecha,
                ),
                ft.Text(self._fecha_recordatorio.strftime("%d/%m/%Y") if self._fecha_recordatorio else "No seleccionada")
            ]
        )

    def _get_hora_inicio(self):
        return ft.Row(
            [
                ft.Text("Hora de inicio"),
                ft.ElevatedButton(
                    text="Seleccionar hora",
                    on_click=self._seleccionar_hora_inicio,
                ),
                ft.Text(self._hora_inicio.format() if self._hora_inicio else "No seleccionada")
            ]
        )

    def _get_hora_fin(self):
        return ft.Row(
            [
                ft.Text("Hora de fin"),
                ft.ElevatedButton(
                    text="Seleccionar hora",
                    on_click=self._seleccionar_hora_fin,
                ),
                ft.Text(self._hora_fin.format() if self._hora_fin else "No seleccionada")
            ]
        )

    def _get_buttons(self):
        return ft.Row(
            [
                ft.ElevatedButton(
                    text="Cancelar",
                    color=ft.colors.RED,
                    on_click=lambda _: self.page.go_back()
                ),
                ft.ElevatedButton(
                    text="Confirmar",
                    color=ft.colors.GREEN,
                    on_click=self._guardar_tarea
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )

    def _seleccionar_fecha(self, e):
        picked_date = self.page.show_date_picker(
            initial_date=self._fecha_recordatorio or ft.Date.now()
        )
        if picked_date:
            self._fecha_recordatorio = picked_date
            self.page.update()

    def _seleccionar_hora_inicio(self, e):
        picked_time = self.page.show_time_picker()
        if picked_time:
            self._hora_inicio = picked_time
            self.page.update()

    def _seleccionar_hora_fin(self, e):
        picked_time = self.page.show_time_picker()
        if picked_time:
            self._hora_fin = picked_time
            self.page.update()

    def _guardar_tarea(self, e):
        if not self._nombre.value or not self._tipo.value:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Todos los campos obligatorios deben ser llenados"),
                open=True,
            )
            return

        db = self.page.database
        tarea = Tarea(
            id=self.tarea.id if self.tarea else None,
            nombre=self._nombre.value,
            descripcion=self._descripcion.value or None,
            tipo=self._tipo.value,
            color=self._color.value,
            lugar_id=self._lugar_id,
            fecha_recordatorio=self._fecha_recordatorio,
            hora_inicio=self._hora_inicio,
            hora_fin=self._hora_fin,
        )

        if self.tarea:
            Tarea.update(db, tarea)
        else:
            Tarea.insert(db, tarea)

        self.page.go_back()
