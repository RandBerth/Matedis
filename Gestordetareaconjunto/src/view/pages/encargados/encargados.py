import flet as ft
from controller import encargado_controller as ec


class EncargadosPage(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.nombre_input = ft.TextField(label="Nombre", expand=True)
        self.correo_input = ft.TextField(label="Correo", expand=True)
        self.lista_encargados = ft.Column()

        self.controls = [
            ft.Text("Registrar Encargado", size=24, weight="bold"),
            ft.Row([
                self.nombre_input,
                self.correo_input,
                ft.ElevatedButton("Agregar", on_click=self.agregar_encargado)
            ]),
            ft.Divider(),
            ft.Text("Lista de Encargados", size=20),
            self.lista_encargados
        ]

        self.cargar_encargados()

    def agregar_encargado(self, e):
        nombre = self.nombre_input.value.strip()
        correo = self.correo_input.value.strip()

        if not nombre or not correo:
            self.page.snack_bar = ft.SnackBar(ft.Text("Completa todos los campos"))
            self.page.snack_bar.open = True
            self.page.update()
            return

        ec.agregar_encargado(nombre, correo)
        self.nombre_input.value = ""
        self.correo_input.value = ""
        self.page.update()
        self.cargar_encargados()

    def eliminar_encargado(self, encargado_id):
        ec.eliminar_encargado(encargado_id)
        self.cargar_encargados()

    def cargar_encargados(self):
        encargados = ec.obtener_encargados()
        self.lista_encargados.controls.clear()

        for id_, nombre, correo in encargados:
            self.lista_encargados.controls.append(
                ft.Card(
                    content=ft.ListTile(
                        title=ft.Text(nombre),
                        subtitle=ft.Text(correo),
                        trailing=ft.IconButton(
                            icon=ft.icons.DELETE,
                            icon_color="red",
                            on_click=lambda e, encargado_id=id_: self.eliminar_encargado(encargado_id)
                        )
                    )
                )
            )
        self.update()
