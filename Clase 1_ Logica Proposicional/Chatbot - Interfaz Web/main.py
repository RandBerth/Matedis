
from Reglas_inferencia import *
from chatbot import *
from nicegui import ui
from fonts import fontScheme
from colors import colorScheme

# Estilos de la interfaz
color_scheme = colorScheme(ui)
font_scheme = fontScheme(color_scheme)

# Inicializamos el bot
fisi_bot = FisiBot()

# El nombre del usuario global
user_name = "Usuario"

# Variables para el modo de inferencia
inference_mode = False

chat_messages = []

def add_message(sender, text, is_user=False, is_system=False):
    """
    Descripción: Agrega un mensaje al chat.
    
    Args:
        sender (str): Nombre del remitente.
        text (str): Texto del mensaje.
        is_user (bool, optional): Define si el mensaje es del usuario. Predeterminado en False.
        is_system (bool, optional): Define si el mensaje es del sistema. Predeterminado en False.
    """
    with chat_container:
        if is_system:
            ui.label(text).classes('bg-purple-100 p-2 rounded-lg self-center text-xs')
        elif is_user:
            with ui.row().classes('w-full flex justify-end'):  
                ui.chat_message(text=text, name=sender, avatar='https://robohash.org/Usuario', sent=True)
        else:
            with ui.row().classes('w-full flex justify-start'):  
                ui.chat_message(text=text, name=sender, avatar='https://robohash.org/Fisibot', sent=False)
    chat_messages.append((sender, text, is_user, is_system))
def handle_inference_input(e):
    """
    Descripción: Procesa las premisas ingresadas por el usuario en el modo de inferencia. Modo que se accede al escribir 'premisa' o 'inferir'.
    
    Args:
        e (Event): Evento de teclado.
    """
    # Obtiene las premisas ingresadas por el usuario
    global inference_mode
    premise_input = inference_input.value
    if not premise_input:
        return
    
    # En caso de que el usuario haya ingresado una premisa, se muestra en el chat
    add_message(user_name, premise_input, is_user=True)
    inference_input.value = ''
    
    # Si el usuario quiere salir del modo inferencia, solo debe ingresar las siguientes palabras clave
    if normalizar(premise_input) in ["salir", "exit", "adios", "chau"]:
        inference_mode = False
        add_message("Fisibotin", f"¡Programa de inferencia lógica cerrado! ¿Puedo ayudarte en algo más, {user_name}?")
        inference_container.set_visibility(False)
        chat_container.set_visibility(True)
        message_input.set_visibility(True)
        inference_input.set_visibility(False)
        return
    
    # Inferiere la conclusión a partir de las premisas ingresadas, desde el archivo Reglas_inferencia.py
    conclusion = infer_conclusion(premise_input)
    add_message("Fisibotin", conclusion)
    add_message("Sistema", "Ingrese otras premisas o escriba 'Salir' para volver al chat normal", is_system=True)

def handle_message_input(e):
    """
    Descripción: Procesa el mensaje ingresado por el usuario en el chat.

    Args:
        e (Event): Evento de teclado.
    """
    
    # Obtiene el mensaje del usuario
    global user_name, inference_mode
    msg = message_input.value
    if not msg:
        return
    
    # Muestra el mensaje del usuario en el chat
    add_message(user_name, msg, is_user=True)
    message_input.value = ''
    
    # Verifica si el usuario quiere salir del chat
    if normalizar(msg) in ["salir", "exit", "adios", "chau"]:
        add_message("Fisibotin", f"¡Hasta luego! Espero haberte ayudado, {user_name}.")
        return
    
    # Verifica si el usuario quiere entrar al modo de inferencia
    if entrar_inferencia(msg):
        inference_mode = True
        add_message("Sistema", "Ingrese las premisas separadas por punto y coma o 'Salir' para volver al chat normal", is_system=True)
        inference_container.set_visibility(True)
        chat_container.set_visibility(True)
        message_input.set_visibility(False)
        inference_input.set_visibility(True)
        return
    
    # Aqui es donde se obtiene la respuesta del chatbot a partir de su clase.
    response = fisi_bot.obtener_respuesta(msg)
    add_message("Fisibotin", response)

def handle_name_input(e):
    """
    Descripción: Procesa el nombre ingresado por el usuario en la bienvenida.

    Args:
        e (Event): Evento de teclado.
    """
    
    # Se almacena el nombre del usuario y se oculta la tarjeta de bienvenida
    global user_name
    name = name_input.value
    if name:
        user_name = name
        welcome_card.set_visibility(False)
        chat_container.set_visibility(True)
        message_input.set_visibility(True)
        add_message("Fisibotin", f"{obtener_saludo()}, {user_name}, ¿En qué puedo ayudarte?")

# -----------------------------------------------------------------------------------------------------------------------------
# Interfaz de la WEB
# -----------------------------------------------------------------------------------------------------------------------------

"""
Sección de la interfaz de usuario utilizando la librería NiceGUI para el chatbot de Fisibotin.
"""

# Encabezado de la página
with ui.card().classes('w-full max-w-3xl mx-auto'):
    with ui.row().classes('flex flex-col items-center justify-center w-full'):
        ui.label('Fisibotin').classes('text-center font-bold text-lg w-full').style(f'f{font_scheme.title}')
        ui.label('Bot de Inferencia Lógica').classes('text-center w-full').style(f'color: {color_scheme.secondary}; f{font_scheme.tab}')
    
# Contenedor de bienvenida, inicialmente visible. Interfaz de usuario para ingresar el nombre.
with ui.card().classes('w-full max-w-3xl mx-auto') as welcome_card:
    ui.label(f'{obtener_saludo()} Soy Fisibotin, tu asistente de inferencia lógica.').classes('text-lg text-center mb-4 ml-8')
    ui.label('¿Cómo deseas que te llame?').classes('text-center ml-8')
    
    with ui.card_section().classes('flex justify-center items-center gap-2 w-full'):
        name_input = ui.input(placeholder='Tu nombre').classes('w-3/4 mr-8')
        ui.button('Comenzar', on_click=handle_name_input).props('color=primary')

# Contenedor del chat. Inicialmente oculto. Interfaz de usuario para ingresar mensajes.
chat_container = ui.card().classes('w-full max-w-3xl mx-auto overflow-y-auto').style('min-height: 400px; max-height: 500px')
chat_container.set_visibility(False)

# Contenedor de la inferencia. Inicialmente oculto. Interfaz de usuario para ingresar premisas.
inference_container = ui.card().classes('w-full max-w-3xl mx-auto mt-2 bg-purple-50 p-2 rounded')
inference_container.set_visibility(False)
with inference_container:
    ui.label('Modo de Inferencia Lógica').classes('text-lg font-bold text-center').style(f'{font_scheme.h2} color: {color_scheme.primary};')
    ui.label('Ingresa tus premisas separadas por punto y coma (;)').classes('text-sm text-center')

# Contenedor de mensajes de chat
message_input = ui.input(placeholder='Escribe tu mensaje...').classes('w-full max-w-3xl mx-auto mt-2')
message_input.on('keydown.enter', handle_message_input)
message_input.set_visibility(False)

# Contenedor de mensajes de inferencia
inference_input = ui.input(placeholder='Escribe tus premisas separadas por ;').classes('w-full max-w-3xl mx-auto mt-2')
inference_input.on('keydown.enter', handle_inference_input)
inference_input.set_visibility(False)

# Ejecución de la web
ui.run(title='Fisibotin - Bot de Inferencia Lógica', favicon='🤖')