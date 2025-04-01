# Fisibot - Chatbot de Inferencia Lógica

Fisibot es un chatbot basado en [NiceGUI](https://github.com/zauberzeug/nicegui) que permite a los usuarios interactuar mediante mensajes y realizar inferencias lógicas en base a premisas ingresadas.

## Características

- **Interfaz amigable** con mensajes tipo chat.
- **Inferencia lógica** a partir de premisas ingresadas por el usuario.
- **Soporte para mensajes del sistema** que guían la interacción.
- **Desplazamiento automático** para mejorar la experiencia de usuario.

## Tecnologías utilizadas

- **Python** (lógica del chatbot e inferencias)
- **NiceGUI** (interfaz gráfica basada en web)
- **JavaScript** (para manejar el desplazamiento automático)

## Instalación y Ejecución

### Prerrequisitos

- Python 3.8 o superior
- pip instalado

### Instalación

```sh
pip install nicegui
pip install pandas
pip install openpyxl
pip install unidecode
pip install fuzzywuzzy
```

También, en caso de ejecución desde Visual Studio Code, probablemente sea necesario la instalación de la extensión CodeRunner.
[Presione aquí](https://marketplace.visualstudio.com/items?itemName=formulahendry.code-runner)

### Ejecución

```sh
python main.py
```

Esto iniciará un servidor local donde se puede acceder a Fisibot desde el navegador. Para que funcione correctamente, asegúrate de estar en la carpeta donde se encuentra main.py antes de ejecutarlo. Puedes navegar hasta la carpeta correcta usando el siguiente comando:

```sh
cd /ruta/del/proyecto
```

Una vez iniciado el servidor, podrás acceder a Fisibot desde tu navegador ingresando la dirección que se mostrará en la terminal (por defecto, suele ser <http://127.0.0.1:8080>).

## Uso

1. **Iniciar conversación** escribiendo mensajes en el chat.
2. **Ingresar premisas** En el chat, escribe premisa, conclusión o inferir, lo que iniciara el modo inferencia. Ingresa premisas separadas por `;` cuando se soliciten.
3. **Obtener inferencias** en base a las premisas ingresadas.
4. **Salir del modo de inferencia** escribiendo `Salir`.

## Problemas conocidos

- El desplazamiento automático puede no funcionar en ciertos navegadores. Se recomienda revisar la implementación en `add_message()`.
- No son perfectas y pueden generar resultados incorrectos o no concluyentes en ciertos casos.

## Colaboradores

- Bayona Vera, Elizabeth Ashley
- Carrascal Castro, María Priscila
- Salcedo Alfaro, Nick Emanuel
