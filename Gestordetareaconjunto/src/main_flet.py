import sys
import os

# Añadir src al path raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import flet as ft
from view.flet_ui.home import main

if __name__ == "__main__":
    ft.app(target=main)