"""
Estilos visuales para widgets ttk de la aplicación.

Centraliza la configuración de Treeview, scrollbars y combobox
para mantener una apariencia uniforme.
"""
from tkinter import ttk
from utils.config import COLORS, FONTS, UI

def setup_style() -> None:
    """
    Configura los estilos globales de Treeview, scrollbars y combobox.
    """
    style = ttk.Style()

    style.configure(
        "Treeview",
        background=COLORS["table_bg"],
        fieldbackground=COLORS["table_bg"],
        foreground=COLORS["text_dark"],
        rowheight=UI["table_row_height"],
        bordercolor=COLORS["border"],
        font=FONTS["table"]
    )

    style.configure(
        "Treeview.Heading",
        background=COLORS["accent"],
        foreground=COLORS["text"],
        font=FONTS["table_heading"],
        padding=(5, 4)
    )

    style.map(
        "Treeview",
        background=[("selected", COLORS["table_selected"])],
        foreground=[("selected", COLORS["text"])]
    )

    style.map(
        "Treeview.Heading",
        background=[("active", COLORS["moss"])],
        foreground=[("active", COLORS["text"])]
    )

    style.configure(
        "TCombobox",
        fieldbackground=COLORS["bg_white"],
        background=COLORS["bg_white"],
        foreground=COLORS["text_dark"],
        bordercolor=COLORS["border"],
        lightcolor=COLORS["border"],
        darkcolor=COLORS["border"],
        arrowcolor=COLORS["text_dark"],
        padding=2,
        relief="flat"
    )

    style.configure(
        "Vertical.TScrollbar",
        background=COLORS["accent"],
        troughcolor=COLORS["bg_white"],
        bordercolor=COLORS["border"],
        arrowcolor=COLORS["text"]
    )
