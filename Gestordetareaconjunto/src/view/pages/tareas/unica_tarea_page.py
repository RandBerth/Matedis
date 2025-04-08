import flet as ft
from model.tarea_model import Tarea
from model.horario_model import Horario
from model.dia_horario_model import DiaHorario
from view.pages.tareas.form_tarea_page import FormTareaPage
from view.pages.tareas.horario_tarea_page import HorarioFormPage

class TareaDetallePage(ft.UserControl):
    def __init__(self, tarea_id):
        super().__init__()
        self.tarea_id = tarea_id
        self.tarea = None
        self.horarios = []

    def build(self):
        self._cargar_tarea_y_horarios()

        if self.tarea is None:
            return ft.Center(ft.Text("Cargando tarea..."))

        content = [
            ft.Text(f"Nombre: {self.tarea.nombre}", size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f"Tipo: {self.tarea.tipo}", size=16),
            ft.Text(f"Descripción: {self.tarea.descripcion or 'Sin descripción'}", size=16),
            ft.Text("Color:", size=16),
            ft.Container(width=50, height=50, bgcolor=self.tarea.color),
            ft.ElevatedButton(
                text="Eliminar Tarea", color=ft.colors.RED, on_click=self._eliminar_tarea
            ),
            ft.ElevatedButton(
                text="Editar Tarea", on_click=self._editar_tarea
            ),
            ft.Text("Horarios de la tarea", size=20, weight=ft.FontWeight.BOLD),
        ]

        if not self.horarios:
            content.append(ft.Text("Aún no hay horarios creados para esta tarea.", size=16, color=ft.colors.GRAY))

        for horario in self.horarios:
            content.append(self._crear_horario_item(horario))

        return ft.Column(content)

    def _cargar_tarea_y_horarios(self):
        db = self.page.database
        self.tarea = Tarea.get_by_id(db, self.tarea_id)
        self.horarios = Horario.get_by_tarea_id(db, self.tarea_id)

    def _eliminar_tarea(self, e):
        dialog = ft.AlertDialog(
            title=ft.Text("Eliminar Tarea"),
            content=ft.Text("¿Estás seguro de eliminar esta tarea?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: dialog.close()),
                ft.ElevatedButton("Eliminar", on_click=self._confirmar_eliminar_tarea)
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _confirmar_eliminar_tarea(self, e):
        db = self.page.database
        try:
            Tarea.delete(db, self.tarea_id)
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Tarea eliminada exitosamente"), open=True)
            self.page.go_back()  # Regresar a la página anterior
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(content=ft.Text(f"Error al eliminar: {str(ex)}"), open=True)

    def _editar_tarea(self, e):
        # Llamar al formulario para editar la tarea
        self.page.add(FormTareaPage(tarea=self.tarea))

    def _crear_horario_item(self, horario):
        dias = self._obtener_dias_del_horario(horario.id)
        dias_text = ', '.join(dias)

        return ft.Card(
            content=ft.ListTile(
                title=f"Horario {horario.id}",
                subtitle=ft.Column([
                    ft.Text(f"{horario.hora_inicio} - {horario.hora_fin}"),
                    ft.Text(f"Días: {dias_text}")
                ]),
                trailing=ft.Row([
                    ft.IconButton(ft.icons.EDIT, on_click=lambda e: self._editar_horario(horario)),
                    ft.IconButton(ft.icons.DELETE, on_click=lambda e: self._eliminar_horario(horario.id)),
                ])
            )
        )

    def _editar_horario(self, horario):
        # Lógica para editar el horario
        self.page.add(HorarioFormPage(tarea_id=self.tarea_id, horario=horario))

    def _eliminar_horario(self, horario_id):
        db = self.page.database
        try:
            Horario.delete(db, horario_id)
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Horario eliminado exitosamente"), open=True)
            self._cargar_tarea_y_horarios()  # Recargar los horarios
            self.update()  # Actualizar la UI
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(content=ft.Text(f"Error al eliminar horario: {str(ex)}"), open=True)

    def _obtener_dias_del_horario(self, horario_id):
        db = self.page.database
        return DiaHorario.get_dias_by_horario_id(db, horario_id)
