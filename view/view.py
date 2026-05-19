import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from typing import Optional, Any
from utils.config import COLORS, UI, FONTS, PREFERRED_PLACEHOLDER
from view.styles import setup_style
from view.widgets import open_calendar


class TaskView(ctk.CTk):
    """
    Ventana principal de la aplicación de gestión de clientes, tareas y reuniones.

    Construye la interfaz gráfica completa con paneles para clientes,
    tareas y reuniones usando CustomTkinter y ttk.
    """

    def __init__(self, controller=None) -> None:
        super().__init__()
        ttk.Style().theme_use("clam")

        self.controller = controller

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("Task & Client Manager")
        self.geometry(UI["window_size"])
        self.minsize(1000, 700)
        self.configure(fg_color=COLORS["bg_main"])

        setup_style()
        self._create_layout()

    #   WIDGETS
    def modern_button(self, parent, text: str, cmd, width: int = 120) -> ctk.CTkButton:
        """
        Crea un botón moderno con el estilo consistente de la aplicación.
        """
        return ctk.CTkButton(
            parent,
            text=text,
            width=width,
            height=UI["button_height"],
            fg_color=COLORS["button_bg"],
            hover_color=COLORS["button_active"],
            text_color=COLORS["text"],
            font=FONTS["button"],
            corner_radius=UI["corner_radius"],
            command=cmd
        )

    def _cal_button(self, parent, target_entry) -> ctk.CTkButton:
        """
        Botón de calendario con estilo consistente.
        """
        return ctk.CTkButton(
            parent,
            text="📅",
            width=34,
            height=UI["input_height"],
            fg_color=COLORS["mist"],
            hover_color=COLORS["accent"],
            text_color=COLORS["text_dark"],
            corner_radius=UI["corner_radius"],
            command=lambda: open_calendar(self, target_entry)
        )

    def _make_date_field(self, parent):
        """
        Entry de fecha + botón calendario en un sub-frame.
        """
        frame = ctk.CTkFrame(parent, fg_color=COLORS["panel_bg"])
        entry = self.modern_entry(frame, width=92, placeholder="DD/MM/YYYY")
        entry.pack(side="left")
        self._cal_button(frame, entry).pack(side="left", padx=(3, 0))
        return frame, entry

    def modern_entry(self, parent, width: int = 160, placeholder: str = "") -> ctk.CTkEntry:
        """
        Crea un campo de entrada con el estilo consistente de la aplicación.
        """
        return ctk.CTkEntry(
            parent,
            height=UI["input_height"],
            width=width,
            fg_color=COLORS["bg_white"],
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text_dark"],
            font=FONTS["input"],
            corner_radius=UI["corner_radius"],
            placeholder_text=placeholder,
            placeholder_text_color=COLORS["accent"]
        )

    def modern_combo(self, parent, values: list, width: int = 140) -> ctk.CTkComboBox:
        """
        Crea un combo box con el estilo consistente de la aplicación.
        """
        return ctk.CTkComboBox(
            parent,
            values=values,
            width=width,
            height=UI["input_height"],
            fg_color=COLORS["bg_white"],
            border_color=COLORS["border"],
            border_width=1,
            text_color=COLORS["text_dark"],
            font=FONTS["input"],
            corner_radius=UI["corner_radius"],
            button_color=COLORS["mist"],
            button_hover_color=COLORS["accent"]
        )
    #   LAYOUT GENERAL
    def _create_layout(self) -> None:
        """
        Construye el layout principal con los tres paneles: clientes, tareas y reuniones.
        """
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=16, pady=16)

        main.grid_rowconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=0, minsize=140)
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)

        self._create_clients_panel(main)
        self.clients_panel.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 10))

        self._create_tasks_panel(main)
        self.tasks_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 8))

        self._create_meetings_panel(main)
        self.meetings_panel.grid(row=1, column=1, sticky="nsew", padx=(8, 0))

    #   CLIENTS PANEL
    def _create_clients_panel(self, parent) -> None:
        """
        Construye el panel de clientes con formulario, botones de acción y tabla.
        """
        self.clients_panel = ctk.CTkFrame(
            parent,
            fg_color=COLORS["panel_bg"],
            corner_radius=UI["corner_radius"]
        )

        # Grid interno: 0 título, 1 form, 2 acciones, 3 separador, 4 treeview (weight=1)
        self.clients_panel.grid_rowconfigure(0, weight=0)
        self.clients_panel.grid_rowconfigure(1, weight=0)
        self.clients_panel.grid_rowconfigure(2, weight=0)
        self.clients_panel.grid_rowconfigure(3, weight=0)
        self.clients_panel.grid_rowconfigure(4, weight=1)
        self.clients_panel.grid_columnconfigure(0, weight=1)
        
        # Título + contador
        title_bar = ctk.CTkFrame(self.clients_panel, fg_color=COLORS["panel_bg"])
        title_bar.grid(row=0, column=0, sticky="ew", padx=16, pady=(10, 4))
        title_bar.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(title_bar, text="CLIENTS", font=FONTS["title"],
                     text_color=COLORS["text_dark"]).grid(row=0, column=0, sticky="w")
        self.clients_count_label = ctk.CTkLabel(title_bar, text="",
                     font=FONTS["label"], text_color=COLORS["moss"])
        self.clients_count_label.grid(row=0, column=1, sticky="e")

        # Formulario — 3 filas en grid (alineación entre columnas)
        form = ctk.CTkFrame(self.clients_panel, fg_color=COLORS["panel_bg"])
        form.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 4))

        for col in (0, 2, 4):
            form.grid_columnconfigure(col, weight=0, minsize=82)
        for col in (1, 3, 5):
            form.grid_columnconfigure(col, weight=1, minsize=120)

        # Fila 0: First Name | Last Name | Email
        ctk.CTkLabel(form, text="First Name:", text_color=COLORS["text_dark"], font=FONTS["label"])\
            .grid(row=0, column=0, padx=(0, 4), pady=2, sticky="w")
        self.name_entry = self.modern_entry(form, width=130, placeholder="First name...")
        self.name_entry.grid(row=0, column=1, padx=(0, 12), pady=2, sticky="ew")

        ctk.CTkLabel(form, text="Last Name:", text_color=COLORS["text_dark"], font=FONTS["label"])\
            .grid(row=0, column=2, padx=(0, 4), pady=2, sticky="w")
        self.last_name_entry = self.modern_entry(form, width=130, placeholder="Last name...")
        self.last_name_entry.grid(row=0, column=3, padx=(0, 12), pady=2, sticky="ew")

        ctk.CTkLabel(form, text="Email:", text_color=COLORS["text_dark"], font=FONTS["label"])\
            .grid(row=0, column=4, padx=(0, 4), pady=2, sticky="w")
        self.email_entry = self.modern_entry(form, width=150, placeholder="name@email.com")
        self.email_entry.grid(row=0, column=5, pady=2, sticky="ew")

        # Fila 1: Phone | Company | Preferred
        ctk.CTkLabel(form, text="Phone:", text_color=COLORS["text_dark"], font=FONTS["label"])\
            .grid(row=1, column=0, padx=(0, 4), pady=2, sticky="w")
        self.phone_entry = self.modern_entry(form, width=130, placeholder="+1 555 000 0000")
        self.phone_entry.grid(row=1, column=1, padx=(0, 12), pady=2, sticky="ew")

        ctk.CTkLabel(form, text="Company:", text_color=COLORS["text_dark"], font=FONTS["label"])\
            .grid(row=1, column=2, padx=(0, 4), pady=2, sticky="w")
        self.company_entry = self.modern_entry(form, width=130, placeholder="Company name...")
        self.company_entry.grid(row=1, column=3, padx=(0, 12), pady=2, sticky="ew")

        ctk.CTkLabel(form, text="Preferred:", text_color=COLORS["text_dark"], font=FONTS["label"])\
            .grid(row=1, column=4, padx=(0, 4), pady=2, sticky="w")
        self.preferred_method_combo = self.modern_combo(
            form, ["Email", "Phone", "WhatsApp", "Telegram", "Instagram", "Other"], width=130)
        self.preferred_method_combo.set("Email")
        self.preferred_method_combo.grid(row=1, column=5, pady=2, sticky="ew")

        # Fila 2: Category | Source
        ctk.CTkLabel(form, text="Category:", text_color=COLORS["text_dark"], font=FONTS["label"])\
            .grid(row=2, column=0, padx=(0, 4), pady=2, sticky="w")
        self.category_combo = self.modern_combo(
            form, ["Client", "Lead", "VIP", "Active", "Inactive", "Prospect"], width=130)
        self.category_combo.grid(row=2, column=1, padx=(0, 12), pady=2, sticky="ew")

        ctk.CTkLabel(form, text="Source:", text_color=COLORS["text_dark"], font=FONTS["label"])\
            .grid(row=2, column=2, padx=(0, 4), pady=2, sticky="w")
        self.source_combo = self.modern_combo(
            form, ["Website", "Referral", "Instagram", "LinkedIn", "Email", "Event", "Other"], width=130)
        self.source_combo.grid(row=2, column=3, padx=(0, 12), pady=2, sticky="ew")

        # Botones de acción y búsqueda
        actions = ctk.CTkFrame(self.clients_panel, fg_color=COLORS["panel_bg"])
        actions.grid(row=2, column=0, sticky="ew", padx=16, pady=(4, 4))

        self.modern_button(actions, "Add Client",    lambda: self.controller.add_client()).pack(side="left", padx=(0, 4))
        self.modern_button(actions, "Edit Client",   self.open_edit_client_popup).pack(side="left", padx=(0, 4))
        self.modern_button(actions, "Delete Client", lambda: self.controller.delete_client()).pack(side="left", padx=(0, 4))
        self.modern_button(actions, "Clear",         self.clear_client_fields).pack(side="left", padx=(0, 18))

        ctk.CTkLabel(actions, text="Search:", text_color=COLORS["text_dark"], font=FONTS["label"]).pack(side="left", padx=(0, 6))
        self.search_entry = self.modern_entry(actions, width=200, placeholder="Search clients...")
        self.search_entry.pack(side="left", padx=(0, 6))
        self.search_entry.bind("<Return>", lambda e: self.search_clients())
        self.modern_button(actions, "🔍", self.search_clients, width=34).pack(side="left")

        # Separador visual entre form y tabla
        ctk.CTkFrame(self.clients_panel, fg_color=COLORS["border"], height=1)\
            .grid(row=3, column=0, sticky="ew", padx=16, pady=(6, 0))

        # Tabla — row=4 (weight=1)
        tree_frame = ctk.CTkFrame(self.clients_panel, fg_color=COLORS["panel_bg"])
        tree_frame.grid(row=4, column=0, sticky="nsew", padx=16, pady=(4, 12))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(1, weight=0)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.clients_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "First Name", "Last Name", "Email", "Phone",
                     "Preferred Method", "Company", "Category", "Source"),
            show="headings"
        )

        for col in ("ID", "First Name", "Last Name", "Email", "Phone",
                    "Preferred Method", "Company", "Category", "Source"):
            self.clients_tree.heading(col, text=col,
                command=lambda c=col: self._sort_column(self.clients_tree, c, False))

        self.clients_tree.column("ID",               width=50,  minwidth=50,  anchor="center", stretch=False)
        self.clients_tree.column("First Name",       width=115, minwidth=90,  anchor="w",      stretch=True)
        self.clients_tree.column("Last Name",        width=115, minwidth=90,  anchor="w",      stretch=True)
        self.clients_tree.column("Email",            width=185, minwidth=130, anchor="w",      stretch=True)
        self.clients_tree.column("Phone",            width=110, minwidth=95,  anchor="center", stretch=False)
        self.clients_tree.column("Preferred Method", width=130, minwidth=110, anchor="w",      stretch=True)
        self.clients_tree.column("Company",          width=120, minwidth=90,  anchor="w",      stretch=True)
        self.clients_tree.column("Category",         width=100, minwidth=80,  anchor="w",      stretch=True)
        self.clients_tree.column("Source",           width=100, minwidth=80,  anchor="w",      stretch=True)

        self.clients_tree.tag_configure("row_even", background=COLORS["bg_white"])
        self.clients_tree.tag_configure("row_odd",  background=COLORS["table_row_alt"])
        self.clients_tree.tag_configure("empty",    foreground=COLORS["accent"])

        clients_vscroll = ttk.Scrollbar(tree_frame, orient="vertical",   command=self.clients_tree.yview)
        clients_hscroll = ttk.Scrollbar(tree_frame, orient="horizontal",  command=self.clients_tree.xview)
        self.clients_tree.configure(
            yscrollcommand=clients_vscroll.set,
            xscrollcommand=clients_hscroll.set
        )

        self.clients_tree.grid(row=0, column=0, sticky="nsew")
        clients_vscroll.grid(row=0, column=1, sticky="ns")
        clients_hscroll.grid(row=1, column=0, sticky="ew")

        self.clients_tree.bind("<<TreeviewSelect>>", lambda e: self.select_client())
        self._bind_tooltip(self.clients_tree, "Email", "Company", "First Name", "Last Name")

    # POPUP EDIT CLIENT
    def open_edit_client_popup(self) -> None:
        """
        Abre una ventana emergente para editar los datos del cliente seleccionado.
        """
        selected = self.clients_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a client to edit.")
            return

        values = self.clients_tree.item(selected[0])["values"]
        client_id = values[0]
        name = values[1]
        last_name = values[2]
        email = values[3]
        phone = values[4]
        preferred_method = values[5]
        company = values[6]
        category = values[7]
        source = values[8]

        top = ctk.CTkToplevel(self)
        top.title("Edit Client")
        top.geometry("520x340")
        top.configure(fg_color=COLORS["panel_bg"])
        top.transient(self)
        top.grab_set()

        form = ctk.CTkFrame(top, fg_color=COLORS["panel_bg"])
        form.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(form, text="First Name:", text_color=COLORS["text_dark"], font=FONTS["label"]).grid(row=0, column=0, padx=6, pady=4, sticky="w")
        name_entry = self.modern_entry(form, width=180)
        name_entry.grid(row=0, column=1, padx=6, pady=4)
        name_entry.insert(0, name)

        ctk.CTkLabel(form, text="Last Name:", text_color=COLORS["text_dark"], font=FONTS["label"]).grid(row=0, column=2, padx=6, pady=4, sticky="w")
        last_name_entry = self.modern_entry(form, width=180)
        last_name_entry.grid(row=0, column=3, padx=6, pady=4)
        last_name_entry.insert(0, last_name)

        ctk.CTkLabel(form, text="Email:", text_color=COLORS["text_dark"], font=FONTS["label"]).grid(row=1, column=0, padx=6, pady=4, sticky="w")
        email_entry = self.modern_entry(form, width=180)
        email_entry.grid(row=1, column=1, padx=6, pady=4)
        email_entry.insert(0, email)

        ctk.CTkLabel(form, text="Phone:", text_color=COLORS["text_dark"], font=FONTS["label"]).grid(row=1, column=2, padx=6, pady=4, sticky="w")
        phone_entry = self.modern_entry(form, width=180)
        phone_entry.grid(row=1, column=3, padx=6, pady=4)
        phone_entry.insert(0, phone)

        ctk.CTkLabel(form, text="Company:", text_color=COLORS["text_dark"], font=FONTS["label"]).grid(row=2, column=0, padx=6, pady=4, sticky="w")
        company_entry = self.modern_entry(form, width=180)
        company_entry.grid(row=2, column=1, padx=6, pady=4)
        company_entry.insert(0, company)

        ctk.CTkLabel(form, text="Category:", text_color=COLORS["text_dark"], font=FONTS["label"]).grid(row=2, column=2, padx=6, pady=4, sticky="w")
        category_combo = self.modern_combo(form, ["Client", "Lead", "VIP", "Active", "Inactive", "Prospect"], width=180)
        category_combo.grid(row=2, column=3, padx=6, pady=4)
        category_combo.set(category)

        ctk.CTkLabel(form, text="Source:", text_color=COLORS["text_dark"], font=FONTS["label"]).grid(row=3, column=0, padx=6, pady=4, sticky="w")
        source_combo = self.modern_combo(form, ["Website", "Referral", "Instagram", "LinkedIn", "Email", "Event", "Other"], width=180)
        source_combo.grid(row=3, column=1, padx=6, pady=4)
        source_combo.set(source)

        ctk.CTkLabel(form, text="Preferred Method:", text_color=COLORS["text_dark"], font=FONTS["label"]).grid(row=3, column=2, padx=6, pady=4, sticky="w")
        preferred_combo = self.modern_combo(form, ["Email", "Phone", "WhatsApp", "Telegram", "Instagram", "Other"], width=180)
        preferred_combo.grid(row=3, column=3, padx=6, pady=4)
        preferred_combo.set(preferred_method or PREFERRED_PLACEHOLDER)

        btns = ctk.CTkFrame(top, fg_color=COLORS["panel_bg"])
        btns.pack(fill="x", padx=16, pady=(0, 12))

        def save():
            self.controller.update_client_from_popup(
                client_id,
                name_entry.get(),
                last_name_entry.get(),
                email_entry.get(),
                phone_entry.get(),
                company_entry.get(),
                category_combo.get(),
                source_combo.get(),
                preferred_combo.get(),
                top
            )

        self.modern_button(btns, "Save", save).pack(side="right", padx=4)
        self.modern_button(btns, "Cancel", top.destroy).pack(side="right", padx=4)


    #   SEARCH CLIENTS
    def search_clients(self) -> None:
        """
        Filtra la tabla de clientes según el texto ingresado en el campo de búsqueda.
        """
        query = self.search_entry.get()
        self.controller.search_clients(query)

    #   TASKS PANEL
    def _create_tasks_panel(self, parent) -> None:
        """
        Construye el panel de tareas con formulario compacto, botones y tabla.
        """
        self.tasks_panel = ctk.CTkFrame(
            parent,
            fg_color=COLORS["panel_bg"],
            corner_radius=UI["corner_radius"]
        )

        # row=0 encabezado compacto (título + form + botones), row=1 tabla
        self.tasks_panel.grid_rowconfigure(0, weight=0)
        self.tasks_panel.grid_rowconfigure(1, weight=1, minsize=30)
        self.tasks_panel.grid_columnconfigure(0, weight=1)

        # ---- Encabezado compacto ----
        header = ctk.CTkFrame(self.tasks_panel, fg_color=COLORS["panel_bg"])
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=(4, 0))

        # Fila 0: título + cliente (izq) | botones (der) — TODO en una línea
        title_row = ctk.CTkFrame(header, fg_color=COLORS["panel_bg"])
        title_row.pack(fill="x", pady=(0, 3))
        ctk.CTkLabel(
            title_row, text="CLIENT TASKS",
            font=FONTS["label_bold"], text_color=COLORS["text_dark"]
        ).pack(side="left")
        self.tasks_client_label = ctk.CTkLabel(
            title_row, text="", font=FONTS["label"], text_color=COLORS["moss"]
        )
        self.tasks_client_label.pack(side="left", padx=(8, 0))
        self.tasks_count_label = ctk.CTkLabel(
            title_row, text="", font=FONTS["label"], text_color=COLORS["accent"]
        )
        self.tasks_count_label.pack(side="left", padx=(8, 0))
        self.modern_button(title_row, "Delete",   lambda: self.controller.delete_task(self.get_selected_client_id())).pack(side="right")
        self.modern_button(title_row, "Edit",     lambda: self.controller.update_task(self.get_selected_client_id())).pack(side="right", padx=(0, 4))
        self.modern_button(title_row, "New Task", lambda: self.controller.add_task(self.get_selected_client_id())).pack(side="right", padx=(0, 4))

        # Formulario — 4 columnas, campos compactos
        form = ctk.CTkFrame(header, fg_color=COLORS["panel_bg"])
        form.pack(fill="x", pady=(0, 4))

        form.grid_columnconfigure(0, weight=0, minsize=58)
        form.grid_columnconfigure(1, weight=2)
        form.grid_columnconfigure(2, weight=0, minsize=72)
        form.grid_columnconfigure(3, weight=1)

        # Fila 0: Task | Status
        ctk.CTkLabel(form, text="Task:", text_color=COLORS["text_dark"], font=FONTS["label"])\
            .grid(row=0, column=0, padx=(0, 4), pady=0, sticky="w")
        self.task_entry = ctk.CTkTextbox(form, height=22, width=200)
        self.task_entry.grid(row=0, column=1, padx=(0, 12), pady=0, sticky="ew")
        ctk.CTkLabel(form, text="Status:", text_color=COLORS["text_dark"], font=FONTS["label"])\
            .grid(row=0, column=2, padx=(0, 4), pady=0, sticky="w")
        self.task_status_combo = self.modern_combo(form, ["Pending", "In Progress", "Completed"], width=120)
        self.task_status_combo.grid(row=0, column=3, pady=0, sticky="ew")

        # Fila 1: Start | Deadline
        ctk.CTkLabel(form, text="Start:", text_color=COLORS["text_dark"], font=FONTS["label"])\
            .grid(row=1, column=0, padx=(0, 4), pady=(2, 0), sticky="w")
        start_frame, self.start_date_entry = self._make_date_field(form)
        start_frame.grid(row=1, column=1, padx=(0, 12), pady=(2, 0), sticky="w")
        ctk.CTkLabel(form, text="Deadline:", text_color=COLORS["text_dark"], font=FONTS["label"])\
            .grid(row=1, column=2, padx=(0, 4), pady=(2, 0), sticky="w")
        deadline_frame, self.deadline_date_entry = self._make_date_field(form)
        deadline_frame.grid(row=1, column=3, pady=(2, 0), sticky="w")

        # ---- Tabla ----
        tree_frame = ctk.CTkFrame(self.tasks_panel, fg_color=COLORS["panel_bg"])
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(2, 4))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.tasks_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Task", "Status", "Start", "Deadline"),
            show="headings"
        )

        for col in ("ID", "Task", "Status", "Start", "Deadline"):
            self.tasks_tree.heading(col, text=col)

        self.tasks_tree.column("ID",       width=48,  minwidth=40,  anchor="center", stretch=False)
        self.tasks_tree.column("Task",     width=200, minwidth=80,  anchor="w",      stretch=True)
        self.tasks_tree.column("Status",   width=110, minwidth=70,  anchor="w",      stretch=True)
        self.tasks_tree.column("Start",    width=100, minwidth=60,  anchor="center", stretch=True)
        self.tasks_tree.column("Deadline", width=100, minwidth=72,  anchor="center", stretch=True)

        self.tasks_tree.tag_configure("row_even", background=COLORS["bg_white"])
        self.tasks_tree.tag_configure("row_odd",  background=COLORS["table_row_alt"])
        self.tasks_tree.tag_configure("empty",    foreground=COLORS["accent"])

        for col in ("ID", "Task", "Status", "Start", "Deadline"):
            self.tasks_tree.heading(col, text=col,
                command=lambda c=col: self._sort_column(self.tasks_tree, c, False))

        tasks_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tasks_tree.yview)
        self.tasks_tree.configure(yscrollcommand=tasks_scroll.set)

        self.tasks_tree.grid(row=0, column=0, sticky="nsew")
        tasks_scroll.grid(row=0, column=1, sticky="ns")

        self.tasks_tree.bind("<Double-1>", lambda e: self._populate_task_form())
        self._bind_tooltip(self.tasks_tree, "Task")

    #   MEETINGS PANEL
    def _create_meetings_panel(self, parent) -> None:
        """
        Construye el panel de reuniones con formulario compacto, botones y tabla.
        """
        self.meetings_panel = ctk.CTkFrame(
            parent,
            fg_color=COLORS["panel_bg"],
            corner_radius=UI["corner_radius"]
        )

        # row=0 encabezado compacto (título + form + botones), row=1 tabla
        self.meetings_panel.grid_rowconfigure(0, weight=0)
        self.meetings_panel.grid_rowconfigure(1, weight=1, minsize=30)
        self.meetings_panel.grid_columnconfigure(0, weight=1)

        # ---- Encabezado compacto ----
        header = ctk.CTkFrame(self.meetings_panel, fg_color=COLORS["panel_bg"])
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=(4, 0))

        # Fila 0: título + cliente (izq) | botones (der) — TODO en una línea
        title_row = ctk.CTkFrame(header, fg_color=COLORS["panel_bg"])
        title_row.pack(fill="x", pady=(0, 3))
        ctk.CTkLabel(
            title_row, text="CLIENT MEETINGS",
            font=FONTS["label_bold"], text_color=COLORS["text_dark"]
        ).pack(side="left")
        self.meetings_client_label = ctk.CTkLabel(
            title_row, text="", font=FONTS["label"], text_color=COLORS["moss"]
        )
        self.meetings_client_label.pack(side="left", padx=(8, 0))
        self.meetings_count_label = ctk.CTkLabel(
            title_row, text="", font=FONTS["label"], text_color=COLORS["accent"]
        )
        self.meetings_count_label.pack(side="left", padx=(8, 0))
        self.modern_button(title_row, "Delete",      lambda: self.controller.delete_meeting(self.get_selected_client_id())).pack(side="right")
        self.modern_button(title_row, "Edit",        lambda: self.controller.update_meeting(self.get_selected_client_id())).pack(side="right", padx=(0, 4))
        self.modern_button(title_row, "New Meeting", lambda: self.controller.add_meeting(self.get_selected_client_id())).pack(side="right", padx=(0, 4))

        # Formulario — 8 columnas, 2 filas compactas
        form = ctk.CTkFrame(header, fg_color=COLORS["panel_bg"])
        form.pack(fill="x", pady=(0, 4))

        form.grid_columnconfigure(0, weight=0, minsize=68)
        form.grid_columnconfigure(1, weight=2)
        form.grid_columnconfigure(2, weight=0, minsize=48)
        form.grid_columnconfigure(3, weight=1)
        form.grid_columnconfigure(4, weight=0, minsize=68)
        form.grid_columnconfigure(5, weight=1)
        form.grid_columnconfigure(6, weight=0, minsize=64)
        form.grid_columnconfigure(7, weight=1)

        # Fila 0: Meeting | Date | Payment | (vacío)
        ctk.CTkLabel(form, text="Meeting:", text_color=COLORS["text_dark"], font=FONTS["label"])\
            .grid(row=0, column=0, padx=(0, 4), pady=0, sticky="w")
        self.meeting_entry = ctk.CTkTextbox(form, height=22, width=170)
        self.meeting_entry.grid(row=0, column=1, padx=(0, 8), pady=0, sticky="ew")
        ctk.CTkLabel(form, text="Date:", text_color=COLORS["text_dark"], font=FONTS["label"])\
            .grid(row=0, column=2, padx=(0, 4), pady=0, sticky="w")
        date_frame, self.meeting_date_entry = self._make_date_field(form)
        date_frame.grid(row=0, column=3, padx=(0, 8), pady=0, sticky="w")
        ctk.CTkLabel(form, text="Payment:", text_color=COLORS["text_dark"], font=FONTS["label"])\
            .grid(row=0, column=4, padx=(0, 4), pady=0, sticky="w")
        self.payment_combo = self.modern_combo(
            form, ["Paid", "Unpaid", "Pending", "Overdue", "Partially Paid", "Refunded", "Cancelled"], width=110)
        self.payment_combo.grid(row=0, column=5, columnspan=3, pady=0, sticky="w")

        # Fila 1: Date Pay | Total | Paid | Method
        ctk.CTkLabel(form, text="Date Pay:", text_color=COLORS["text_dark"], font=FONTS["label"])\
            .grid(row=1, column=0, padx=(0, 4), pady=(2, 0), sticky="w")
        datepay_frame, self.payment_date_entry = self._make_date_field(form)
        datepay_frame.grid(row=1, column=1, padx=(0, 8), pady=(2, 0), sticky="w")
        ctk.CTkLabel(form, text="Total:", text_color=COLORS["text_dark"], font=FONTS["label"])\
            .grid(row=1, column=2, padx=(0, 4), pady=(2, 0), sticky="w")
        self.total_entry = self.modern_entry(form, width=80, placeholder="0.00")
        self.total_entry.grid(row=1, column=3, padx=(0, 8), pady=(2, 0), sticky="w")
        ctk.CTkLabel(form, text="Paid:", text_color=COLORS["text_dark"], font=FONTS["label"])\
            .grid(row=1, column=4, padx=(0, 4), pady=(2, 0), sticky="w")
        self.paid_entry = self.modern_entry(form, width=80, placeholder="0.00")
        self.paid_entry.grid(row=1, column=5, padx=(0, 8), pady=(2, 0), sticky="w")
        ctk.CTkLabel(form, text="Method:", text_color=COLORS["text_dark"], font=FONTS["label"])\
            .grid(row=1, column=6, padx=(0, 4), pady=(2, 0), sticky="w")
        self.payment_method_combo = self.modern_combo(
            form, ["Cash", "Credit Card", "Debit Card", "Bank Transfer", "MercadoPago", "Other"], width=118)
        self.payment_method_combo.set("Payment Method")
        self.payment_method_combo.grid(row=1, column=7, pady=(2, 0), sticky="ew")

        # ---- Tabla ----
        tree_frame = ctk.CTkFrame(self.meetings_panel, fg_color=COLORS["panel_bg"])
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(2, 4))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.meetings_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Meeting", "Date", "Date Pay", "Status", "Total", "Paid", "Method"),
            show="headings"
        )

        self.meetings_tree.tag_configure("paid",      background="#D4F8D4")
        self.meetings_tree.tag_configure("unpaid",    background="#F8D4D4")
        self.meetings_tree.tag_configure("pending",   background="#FFF4C2")
        self.meetings_tree.tag_configure("overdue",   background="#FFB3B3")
        self.meetings_tree.tag_configure("partial",   background="#FFE9C6")
        self.meetings_tree.tag_configure("refunded",  background="#D4E6F8")
        self.meetings_tree.tag_configure("cancelled", background="#E0E0E0")
        self.meetings_tree.tag_configure("empty",     foreground=COLORS["accent"])

        for col in ("ID", "Meeting", "Date", "Date Pay", "Status", "Total", "Paid", "Method"):
            self.meetings_tree.heading(col, text=col,
                command=lambda c=col: self._sort_column(self.meetings_tree, c, False))

        self.meetings_tree.column("ID",       width=48,  minwidth=40,  anchor="center", stretch=False)
        self.meetings_tree.column("Meeting",  width=175, minwidth=70,  anchor="w",      stretch=True)
        self.meetings_tree.column("Date",     width=92,  minwidth=48,  anchor="center", stretch=True)
        self.meetings_tree.column("Date Pay", width=92,  minwidth=68,  anchor="center", stretch=True)
        self.meetings_tree.column("Status",   width=100, minwidth=62,  anchor="w",      stretch=True)
        self.meetings_tree.column("Total",    width=80,  minwidth=48,  anchor="e",      stretch=True)
        self.meetings_tree.column("Paid",     width=80,  minwidth=42,  anchor="e",      stretch=True)
        self.meetings_tree.column("Method",   width=110, minwidth=62,  anchor="w",      stretch=True)

        meetings_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.meetings_tree.yview)
        self.meetings_tree.configure(yscrollcommand=meetings_scroll.set)

        self.meetings_tree.grid(row=0, column=0, sticky="nsew")
        meetings_scroll.grid(row=0, column=1, sticky="ns")

        self.meetings_tree.bind("<Double-1>", lambda e: self._populate_meeting_form())
        self._bind_tooltip(self.meetings_tree, "Meeting")

    #   HELPERS
    def update_clients_table(self, clients: list) -> None:
        """
        Actualiza la tabla de clientes con la lista proporcionada y aplica formato zebra.
        """
        self._clear_tree(self.clients_tree)
        n = len(clients)
        self.clients_count_label.configure(text=f"({n})" if n else "")
        if clients:
            for i, c in enumerate(clients):
                tag = "row_even" if i % 2 == 0 else "row_odd"
                self.clients_tree.insert("", "end", values=c, tags=(tag,))
        else:
            self.clients_tree.insert("", "end",
                values=("", "No clients found", "", "", "", "", "", "", ""),
                tags=("empty",))

    def get_selected_client_id(self) -> Optional[int]:
        """
        Retorna el ID del cliente seleccionado en la tabla o None si no hay selección.
        """
        selected = self.clients_tree.selection()
        if not selected:
            return None
        return self.clients_tree.item(selected[0])["values"][0]

    def clear_client_fields(self) -> None:
        """
        Limpia todos los campos del formulario de clientes.
        """
        for entry in [
            self.name_entry,
            self.last_name_entry,
            self.email_entry,
            self.phone_entry,
            self.company_entry
        ]:
            entry.delete(0, "end")
        self.category_combo.set("")
        self.source_combo.set("")
        self.preferred_method_combo.set("Email")
        self.search_entry.delete(0, "end")

    def select_client(self) -> None:
        """
        Maneja la selección de un cliente: actualiza título, tareas y reuniones.
        """
        client_id = self.get_selected_client_id()
        if client_id:
            selected = self.clients_tree.selection()
            vals = self.clients_tree.item(selected[0])["values"]
            name = f"{vals[1]} {vals[2]}"
            self.tasks_client_label.configure(text=f"— {name}")
            self.meetings_client_label.configure(text=f"— {name}")
            self.title(f"Task & Client Manager — {name}")
            self.controller.load_tasks(client_id)
            self.controller.load_meetings(client_id)
        else:
            self.tasks_client_label.configure(text="")
            self.meetings_client_label.configure(text="")
            self.title("Task & Client Manager")
            self.update_tasks_table([])
            self.update_meetings_table([])

    def update_tasks_table(self, tasks: list) -> None:
        """
        Actualiza la tabla de tareas con la lista proporcionada y aplica formato zebra.
        """
        self._clear_tree(self.tasks_tree)
        n = len(tasks)
        self.tasks_count_label.configure(text=f"({n})" if n else "")
        if tasks:
            for i, t in enumerate(tasks):
                tag = "row_even" if i % 2 == 0 else "row_odd"
                self.tasks_tree.insert("", "end", values=t, tags=(tag,))
        else:
            has_client = bool(self.tasks_client_label.cget("text"))
            msg = "No tasks for this client" if has_client else "Select a client to view tasks"
            self.tasks_tree.insert("", "end",
                values=("", msg, "", "", ""), tags=("empty",))

    def get_selected_task_id(self) -> Optional[int]:
        """
        Retorna el ID de la tarea seleccionada en la tabla o None si no hay selección.
        """
        selected = self.tasks_tree.selection()
        if not selected:
            return None
        return self.tasks_tree.item(selected[0])["values"][0]

    def update_meetings_table(self, meetings: list) -> None:
        """
        Actualiza la tabla de reuniones aplicando colores según el estado de pago.
        """
        self._clear_tree(self.meetings_tree)
        n = len(meetings)
        self.meetings_count_label.configure(text=f"({n})" if n else "")
        if not meetings:
            has_client = bool(self.meetings_client_label.cget("text"))
            msg = "No meetings for this client" if has_client else "Select a client to view meetings"
            self.meetings_tree.insert("", "end",
                values=("", msg, "", "", "", "", "", ""), tags=("empty",))
            return

        for m in meetings:
            payment = str(m[3]).lower()

            if payment == "paid":
                tag = "paid"
            elif payment == "unpaid":
                tag = "unpaid"
            elif payment == "pending":
                tag = "pending"
            elif payment == "overdue":
                tag = "overdue"
            elif payment == "partially paid":
                tag = "partial"
            elif payment == "refunded":
                tag = "refunded"
            elif payment == "cancelled":
                tag = "cancelled"
            else:
                tag = ""

            values = (m[0], m[1], m[2], m[7], m[3], m[4], m[5], m[6])
            self.meetings_tree.insert("", "end", values=values, tags=(tag,))

    def get_selected_meeting_id(self) -> Optional[int]:
        """
        Retorna el ID de la reunión seleccionada en la tabla o None si no hay selección.
        """
        selected = self.meetings_tree.selection()
        if not selected:
            return None
        return self.meetings_tree.item(selected[0])["values"][0]

    def _populate_task_form(self) -> None:
        """
        Rellena el formulario de tareas con los datos de la tarea seleccionada.
        """
        selected = self.tasks_tree.selection()
        if not selected:
            return
        values = self.tasks_tree.item(selected[0])["values"]
        # values: (ID, Task, Status, Start, Deadline)
        self.task_entry.delete("1.0", "end")
        self.task_entry.insert("1.0", values[1])
        self.task_status_combo.set(values[2])
        self.start_date_entry.delete(0, "end")
        self.start_date_entry.insert(0, values[3])
        self.deadline_date_entry.delete(0, "end")
        self.deadline_date_entry.insert(0, values[4])

    def _populate_meeting_form(self) -> None:
        """
        Rellena el formulario de reuniones con los datos de la reunión seleccionada.
        """
        selected = self.meetings_tree.selection()
        if not selected:
            return
        values = self.meetings_tree.item(selected[0])["values"]
        # values: (ID, Meeting, Date, Date Pay, Status, Total, Paid, Method)
        self.meeting_entry.delete("1.0", "end")
        self.meeting_entry.insert("1.0", values[1])
        self.meeting_date_entry.delete(0, "end")
        self.meeting_date_entry.insert(0, values[2])
        self.payment_date_entry.delete(0, "end")
        self.payment_date_entry.insert(0, values[3])
        self.payment_combo.set(values[4])
        self.total_entry.delete(0, "end")
        self.total_entry.insert(0, values[5])
        self.paid_entry.delete(0, "end")
        self.paid_entry.insert(0, values[6])
        method = values[7] if values[7] else "Payment Method"
        self.payment_method_combo.set(method)

    def _sort_column(self, tree, col: str, reverse: bool) -> None:
        """
        Ordena una columna de la tabla de forma ascendente o descendente al hacer clic.
        """
        items = [(tree.set(k, col), k) for k in tree.get_children("")]
        try:
            items.sort(key=lambda t: float(t[0]) if t[0] else 0, reverse=reverse)
        except ValueError:
            items.sort(key=lambda t: str(t[0]).lower(), reverse=reverse)
        for idx, (_, k) in enumerate(items):
            tree.move(k, "", idx)
        # Resetear todos los headings y marcar la columna ordenada
        for c in tree["columns"]:
            tree.heading(c, text=c,
                command=lambda _c=c: self._sort_column(tree, _c, False))
        tree.heading(col, text=col + (" ▲" if not reverse else " ▼"),
                     command=lambda: self._sort_column(tree, col, not reverse))
        # Reaplica zebra solo en tablas que la usan (no meetings — tiene colores de pago)
        if tree in (self.clients_tree, self.tasks_tree):
            self._reapply_zebra(tree)

    def _reapply_zebra(self, tree) -> None:
        """
        Reaplica el coloreado alternado de filas después de ordenar la tabla.
        """
        for i, row in enumerate(tree.get_children()):
            tree.item(row, tags=("row_even" if i % 2 == 0 else "row_odd",))

    def _bind_tooltip(self, tree, *col_names: str) -> None:
        """
        Muestra el texto completo de columnas al hacer hover (acepta múltiples columnas).
        """
        col_set = set(col_names)
        tip = {"win": None}

        def show(x, y, text):
            hide()
            tw = tk.Toplevel(tree)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{x}+{y}")
            tk.Label(
                tw, text=text, justify="left",
                background="#FFFBE6", foreground=COLORS["soot"],
                relief="solid", borderwidth=1,
                wraplength=460, padx=10, pady=6,
                font=("Segoe UI", 12)
            ).pack()
            tip["win"] = tw

        def hide(*_):
            if tip["win"]:
                try:
                    tip["win"].destroy()
                except Exception:
                    pass
                tip["win"] = None

        def on_motion(event):
            item = tree.identify_row(event.y)
            col  = tree.identify_column(event.x)
            if item and col:
                idx = int(col[1:]) - 1
                cols = tree["columns"]
                if idx < len(cols) and cols[idx] in col_set:
                    text = tree.set(item, cols[idx])
                    if text:
                        show(event.x_root + 16, event.y_root + 16, text)
                        return
            hide()

        tree.bind("<Motion>", on_motion, add=True)
        tree.bind("<Leave>",  hide, add=True)

    def _clear_tree(self, tree) -> None:
        """
        Elimina todas las filas de una tabla Treeview.
        """
        for row in tree.get_children():
            tree.delete(row)
