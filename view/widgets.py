"""
Widgets reutilizables para la interfaz de usuario.

Actualmente proporciona un selector de calendario modal
que permite elegir fechas y escribirlas en un campo de entrada.
"""
import tkinter as tk
import calendar
from datetime import datetime
from utils.config import COLORS, FONTS

def open_calendar(parent: tk.Misc, target_entry: tk.Entry) -> None:
    """
    Abre un calendario emergente para seleccionar una fecha.

    La fecha seleccionada se inserta automáticamente en el campo
    target_entry con formato DD/MM/YYYY.

    Args:
        parent: Ventana padre sobre la que se muestra el calendario.
        target_entry: Widget de entrada donde se escribirá la fecha.
    """
    top = tk.Toplevel(parent)
    top.title("Seleccionar Fecha")
    top.configure(bg=COLORS["bg_main"])

    # Ajuste automático para Windows DPI
    top.update_idletasks()
    top.geometry("300x330")  # un poco más grande para evitar recortes
    top.resizable(True, True)  # permitir expansión si Windows lo necesita

    # Posicionar cerca del entry que abrió el calendario
    x = parent.winfo_rootx() + 80
    y = parent.winfo_rooty() + 120
    top.geometry(f"+{x}+{y}")

    top.attributes("-topmost", True)
    top.attributes("-alpha", 0.97)

    bg = COLORS["bg_white"]
    accent = COLORS["accent"]
    text = COLORS["text_dark"]
    border = COLORS["border"]

    cal_frame = tk.Frame(
        top,
        bg=bg,
        bd=1,
        relief="solid",
        highlightbackground=border,
        highlightthickness=1
    )
    cal_frame.pack(padx=12, pady=12, fill="both", expand=True)
    cal_frame.pack_propagate(True)  # evita recortes internos

    now = datetime.now()
    year = now.year
    month = now.month

    header = tk.Frame(cal_frame, bg=bg)
    header.pack(fill="x", pady=6)

    month_var = tk.StringVar()
    month_var.set(f"{calendar.month_name[month]} {year}")

    tk.Button(
        header,
        text="◀",
        bg=bg,
        fg=text,
        bd=0,
        font=FONTS["label"],
        command=lambda: change_month(-1)
    ).pack(side="left", padx=4)

    tk.Label(
        header,
        textvariable=month_var,
        bg=bg,
        fg=text,
        font=FONTS["label_bold"]
    ).pack(side="left", expand=True)

    tk.Button(
        header,
        text="▶",
        bg=bg,
        fg=text,
        bd=0,
        font=FONTS["label"],
        command=lambda: change_month(1)
    ).pack(side="right", padx=4)

    days_frame = tk.Frame(cal_frame, bg=bg)
    days_frame.pack(fill="both", expand=True)

    selected_day = tk.StringVar()

    def draw_calendar(y, m):
        for widget in days_frame.winfo_children():
            widget.destroy()

        # Encabezados de días
        for i, day in enumerate(["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]):
            tk.Label(
                days_frame,
                text=day,
                bg=bg,
                fg=text,
                font=FONTS["label_bold"]
            ).grid(row=0, column=i, pady=2)

        month_days = calendar.monthcalendar(y, m)

        for r, week in enumerate(month_days, start=1):
            for c, day in enumerate(week):
                if day == 0:
                    continue

                btn = tk.Button(
                    days_frame,
                    text=str(day),
                    bg=bg,
                    fg=text,
                    bd=1,
                    relief="solid",
                    highlightbackground=border,
                    highlightthickness=1,
                    width=4,   # más grande para evitar recortes
                    height=2,  # más alto para Windows
                    font=FONTS["label"],
                    activebackground=accent,
                    activeforeground=COLORS["text"],
                    command=lambda d=day: select_day(d)
                )
                btn.grid(row=r, column=c, padx=2, pady=2)

    def change_month(delta):
        nonlocal month, year
        month += delta
        if month < 1:
            month = 12
            year -= 1
        elif month > 12:
            month = 1
            year += 1

        month_var.set(f"{calendar.month_name[month]} {year}")
        draw_calendar(year, month)

    def select_day(day):
        selected_day.set(f"{day:02d}/{month:02d}/{year}")

    footer = tk.Frame(cal_frame, bg=bg)
    footer.pack(fill="x", pady=6)

    tk.Button(
        footer,
        text="Cancelar",
        bg=COLORS["bg_main"],
        fg=text,
        bd=0,
        padx=8,
        pady=4,
        font=FONTS["button"],
        command=top.destroy
    ).pack(side="left", padx=4)

    tk.Button(
        footer,
        text="Aceptar",
        bg=accent,
        fg=COLORS["text"],
        bd=0,
        padx=8,
        pady=4,
        font=FONTS["button"],
        command=lambda: apply_date()
    ).pack(side="right", padx=4)

    def apply_date():
        if selected_day.get():
            target_entry.delete(0, tk.END)
            target_entry.insert(0, selected_day.get())
        top.destroy()

    draw_calendar(year, month)
