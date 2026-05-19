"""
Configuración centralizada de la aplicación.

Define colores, fuentes, medidas de UI y formatos usados en toda
la interfaz para mantener consistencia visual y facilitar cambios. 
"""
import platform
_WIN = platform.system() == "Windows"

# PALETA DE COLORES
COLORS = {
    # Fondo general
    "bg_main": "#B3C9D6",
    
    # Paneles y entradas blancas
    "bg_white": "#FFFFFF",
    "panel_bg": "#FFFFFF",
    
    # Encabezados y acentos
    "accent": "#98AA9D",
    
    # Texto
    "text": "#FFFFFF",
    "text_dark": "#2D3536",
    
    # Bordes
    "border": "#697C70",
    
    # Botones principales
    "button_bg": "#98AA9D",
    "button_active": "#7F968A",
    
    # Tablas
    "table_bg": "#FFFFFF",
    "table_selected": "#98AA9D",
    "table_row_alt": "#E8F0EC",
    
    # Paleta Completa
    "eucalyptus": "#98AA9D",
    "moss": "#697C70",
    "soot": "#2D3536",
    "mist": "#B3C9D6"
}

# TIPOGRAFIAS
FONTS = {
    "title": ("Segoe UI", 16, "bold"),
    "subtitle": ("Segoe UI", 14, "bold"),
    "label": ("Segoe UI", 13),
    "label_bold": ("Segoe UI", 13, "bold"),
    "input": ("Segoe UI", 13),
    "button": ("Segoe UI", 13, "bold"),
    # Windows necesita fuente mas prqueña en tabla para cortar texto
    "table":         ("Segoe UI", 12) if _WIN else ("Segoe UI", 13),
    "table_heading": ("Segoe UI", 12, "bold") if _WIN else ("Segoe UI", 13, "bold"),
}

# CONFIGURACION DE UI
UI = {
    "window_size": "1300x870",
    "padding": 14,
    "corner_radius": 10,
    "input_height": 30, 
    "button_height": 30,
    "textbox_height": 50,
    # Windows necesita mas altura por el padding interno del tema nativo
    "table_row_height": 48 if _WIN else 42,
}

# CONSTANTES
PREFERRED_PLACEHOLDER = "Preferred Contact Method"

# FORMATOS
FORMATS = {
    "date": "%d/%m/%Y",
}