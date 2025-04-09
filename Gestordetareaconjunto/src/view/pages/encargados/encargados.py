import flet as ft
from controller import encargado_controller as ec

def EncargadosPage(page):
    """Función que crea la página de encargados"""
    
    # Componentes
    nombre_input = ft.TextField(label="Nombre", expand=True)
    contacto_input = ft.TextField(label="Contacto", expand=True)
    lista_encargados = ft.Column()
    
    def agregar_encargado(e):
        """Agrega un nuevo encargado a la base de datos"""
        nombre = nombre_input.value.strip()
        contacto = contacto_input.value.strip()

        if not nombre or not contacto:
            page.snack_bar = ft.SnackBar(ft.Text("Completa todos los campos"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            ec.agregar_encargado(nombre, contacto)
            nombre_input.value = ""
            contacto_input.value = ""
            page.update()
            cargar_encargados()
            
            # Mostrar mensaje de éxito
            page.snack_bar = ft.SnackBar(ft.Text("Encargado agregado correctamente"))
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            # Mostrar mensaje de error
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"))
            page.snack_bar.open = True
            page.update()

    def eliminar_encargado(e, encargado_id):
        """Elimina un encargado de la base de datos"""
        try:
            ec.eliminar_encargado(encargado_id)
            cargar_encargados()
            
            # Mostrar mensaje de éxito
            page.snack_bar = ft.SnackBar(ft.Text("Encargado eliminado correctamente"))
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            # Mostrar mensaje de error
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"))
            page.snack_bar.open = True
            page.update()

    def cargar_encargados():
        """Carga la lista de encargados desde la base de datos"""
        try:
            encargados = ec.obtener_encargados()
            lista_encargados.controls.clear()

            if not encargados:
                lista_encargados.controls.append(
                    ft.Text("No hay encargados registrados", italic=True)
                )
            else:
                for id_, nombre, contacto in encargados:
                    lista_encargados.controls.append(
                        ft.Card(
                            content=ft.ListTile(
                                title=ft.Text(nombre),
                                subtitle=ft.Text(contacto),
                                trailing=ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    icon_color="red",
                                    on_click=lambda e, id=id_: eliminar_encargado(e, id)
                                )
                            )
                        )
                    )
            
            # Actualizar la página después de modificar los controles
            page.update()
        except Exception as ex:
            print(f"Error al cargar encargados: {ex}")
            lista_encargados.controls.append(
                ft.Text(f"Error al cargar encargados: {str(ex)}", color="red")
            )
            page.update()
    
    # Crear la estructura de la página
    contenido = ft.Column([
        ft.Text("Registrar Encargado", size=24, weight="bold"),
        ft.Row([
            nombre_input,
            contacto_input,
            ft.ElevatedButton("Agregar", on_click=agregar_encargado)
        ]),
        ft.Divider(),
        ft.Text("Lista de Encargados", size=20),
        lista_encargados
    ])
    
    # Cargar los encargados inicialmente
    cargar_encargados()
    
    return contenido