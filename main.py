"""
Punto de entrada principal de la aplicación.

Configura el DPI scaling para Windows, crea la vista y el controlador,
e inicia el bucle principal de la interfaz gráfica.

Nota: el bloque ``if __name__ == "__main__"`` al final del archivo
garantiza que ``main()`` solo se ejecute cuando este archivo se corre
directamente (``python main.py``) y NO cuando se importa desde otro
módulo. Es el estándar de Python para separar código ejecutable de
código reutilizable.
"""

import ctypes
from controllers.controller import Controller
from view.view import TaskView
from model.database import create_tables

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

def main():
    """
    Inicializa y ejecuta la aplicación.
    """
    # Crear tablas de la DB si no existen
    create_tables()
    # Crear la vista primero (UI moderna)
    view = TaskView()
    # Forzar tamaño mínimo para evitar recortes en Windows
    view.minsize(1200, 700)
    # Abrir maximizada automáticamente (Windows necesita esto)
    view.after(100, lambda: view.state("zoomed"))
    # Crear el controller y conectarlo a la vista
    controller = Controller()
    controller.set_view(view)
    # Pasar el controller a la vista
    view.controller = controller
    # Cargar clientes al iniciar
    controller.load_clients()
    # Iniciar la app
    view.mainloop()

if __name__ == "__main__":
    main()