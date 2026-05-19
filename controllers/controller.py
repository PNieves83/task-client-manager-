from tkinter import messagebox
from typing import Optional
from model.model import Model
from model.validators import Validators
from utils.config import PREFERRED_PLACEHOLDER


class Controller:
    """
    Controlador principal de la aplicación.

    Coordina la comunicación entre la vista (interfaz gráfica) y el
    modelo (base de datos), aplicando validaciones antes de cada
    operación.
    """
    def __init__(self, view=None) -> None:
        self.model = Model()
        self.view = view

    def set_view(self, view) -> None:
        """
        Asigna la vista al controlador y permite la comunicación bidireccional.
        """
        self.view = view

    def get_all_clients(self) -> list:
        """
        Retorna la lista completa de clientes desde el modelo.
        """
        return self.model.get_clients()

    # CLIENTES
    def add_client(self) -> None:
        name = self.view.name_entry.get()
        last_name = self.view.last_name_entry.get()
        email = self.view.email_entry.get()
        phone = self.view.phone_entry.get()
        company = self.view.company_entry.get()
        category = self.view.category_combo.get()
        source = self.view.source_combo.get()
        preferred_method = self.view.preferred_method_combo.get()
        if preferred_method == PREFERRED_PLACEHOLDER:
            preferred_method = None

        errors = [
            Validators.validate_name(name, "Name"),
            Validators.validate_name(last_name, "Last Name"),
            Validators.validate_email(email, "Email"),
            Validators.validate_phone(phone, "Phone"),
        ]
        errors = [e for e in errors if e]

        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        try:
            new_id = self.model.add_client(
                name, last_name, email, phone,
                company, category, source, preferred_method
            )
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        messagebox.showinfo("Success", "Client added successfully.")

        self.load_clients()
        self._select_client_in_table(new_id)

        self.view.clear_client_fields()

    def _select_client_in_table(self, client_id: int) -> None:
        """
        Selecciona automáticamente el cliente recién creado.
        """
        tree = self.view.clients_tree
        for item in tree.get_children():
            if tree.item(item)["values"][0] == client_id:
                tree.selection_set(item)
                tree.focus(item)
                tree.see(item)
                self.view.select_client()
                break

    def load_clients(self) -> None:
        """
        Carga todos los clientes y actualiza la tabla en la vista.
        """
        clients = self.model.get_clients()
        self.view.update_clients_table(clients)

    def search_clients(self, query: str) -> None:
        """
        Filtra clientes por texto y actualiza la tabla en la vista.
        """
        if not query.strip():
            self.load_clients()
            return
        all_clients = self.model.get_clients()
        query_lower = query.lower().strip()
        filtered = [
            c for c in all_clients
            if any(query_lower in str(field).lower() for field in c)
        ]
        self.view.update_clients_table(filtered)

    def delete_client(self) -> None:
        """
        Elimina el cliente seleccionado tras confirmación del usuario.
        """
        client_id = self.view.get_selected_client_id()

        if not client_id:
            messagebox.showwarning("Warning", "Select a client to delete.")
            return

        selected = self.view.clients_tree.selection()
        vals = self.view.clients_tree.item(selected[0])["values"]
        name = f"{vals[1]} {vals[2]}"
        if not messagebox.askyesno("Confirm Delete",
                f"Delete client '{name}' and all their tasks and meetings?\nThis cannot be undone."):
            return

        try:
            self.model.delete_client(client_id)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        self.load_clients()
        self.view.update_tasks_table([])
        self.view.update_meetings_table([])

    def update_client_from_popup(
        self,
        client_id: int,
        name: str,
        last_name: str,
        email: str,
        phone: str,
        company: str,
        category: str,
        source: str,
        preferred_method: str,
        window
    ) -> None:
        """
        Actualiza un cliente desde la ventana emergente de edición.
        """
        if preferred_method == PREFERRED_PLACEHOLDER:
            preferred_method = None

        errors = [
            Validators.validate_name(name, "Name"),
            Validators.validate_name(last_name, "Last Name"),
            Validators.validate_email(email, "Email"),
            Validators.validate_phone(phone, "Phone"),
        ]
        errors = [e for e in errors if e]

        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors), parent=window)
            return

        try:
            self.model.update_client(
                client_id, name, last_name, email, phone,
                company, category, source, preferred_method
            )
        except Exception as e:
            messagebox.showerror("Database Error", str(e), parent=window)
            return

        messagebox.showinfo("Success", "Client updated.", parent=window)
        window.destroy()
        self.load_clients()

    # TAREAS
    def load_tasks(self, client_id: int) -> None:
        """
        Carga las tareas de un cliente y actualiza la tabla en la vista.
        """
        tasks = self.model.get_tasks_by_client(client_id)
        self.view.update_tasks_table(tasks)

    def add_task(self, client_id: int) -> None:
        """
        Valida los datos y agrega una nueva tarea para el cliente seleccionado.
        """
        task = self.view.task_entry.get("1.0", "end").strip()
        task_status = self.view.task_status_combo.get()
        start_date = self.view.start_date_entry.get()
        deadline = self.view.deadline_date_entry.get()

        errors = [Validators.validate_required(task, "Task")]

        # Fechas futuras permitidas (Opción C)
        if task_status.lower() != "completed":
            errors.append(Validators.validate_date(start_date, "Start Date", allow_future=True))
            errors.append(Validators.validate_date(deadline, "Deadline", allow_future=True))

        errors = [e for e in errors if e]

        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        try:
            new_id = self.model.add_task(client_id, task, task_status, start_date, deadline)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        messagebox.showinfo("Success", "Task added.")
        self.load_tasks(client_id)

    def update_task(self, client_id: int) -> None:
        """
        Valida y actualiza la tarea seleccionada del cliente.
        """
        task_id = self.view.get_selected_task_id()
        if not task_id:
            messagebox.showwarning("Warning", "Select a task to update.")
            return

        task = self.view.task_entry.get("1.0", "end").strip()
        task_status = self.view.task_status_combo.get()
        start_date = self.view.start_date_entry.get()
        deadline = self.view.deadline_date_entry.get()

        errors = [Validators.validate_required(task, "Task")]

        if task_status.lower() != "completed":
            errors.append(Validators.validate_date(start_date, "Start Date", allow_future=True))
            errors.append(Validators.validate_date(deadline, "Deadline", allow_future=True))

        errors = [e for e in errors if e]

        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        try:
            self.model.update_task(task_id, task, task_status, start_date, deadline)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        messagebox.showinfo("Success", "Task updated.")
        self.load_tasks(client_id)

    def delete_task(self, client_id: int) -> None:
        """
        Elimina la tarea seleccionada tras confirmación del usuario.
        """
        task_id = self.view.get_selected_task_id()
        if not task_id:
            messagebox.showwarning("Warning", "Select a task to delete.")
            return

        selected = self.view.tasks_tree.selection()
        task_name = self.view.tasks_tree.item(selected[0])["values"][1]
        if not messagebox.askyesno("Confirm Delete",
                f"Delete task '{task_name}'?\nThis cannot be undone."):
            return

        try:
            self.model.delete_task(task_id)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        self.load_tasks(client_id)

    # REUNIONES
    def load_meetings(self, client_id: int) -> None:
        """
        Carga las reuniones de un cliente y actualiza la tabla en la vista.
        """
        meetings = self.model.get_meetings_by_client(client_id)
        self.view.update_meetings_table(meetings)

    def _parse_amount(self, value: str, field_name: str):
        """
        Convierte montos y usa Validators para validar.
        """
        value = (value or "").strip()
        err = Validators.validate_amount(value, field_name)
        if err:
            return 0.0, err

        if not value:
            return 0.0, None

        return float(value.replace(",", ".")), None

    def _validate_meeting_data(self):
        """
        Extrae y valida los datos del formulario de reuniones.

        Returns:
            dict | None: Diccionario con datos validados o None si hay errores.
        """
        meeting = self.view.meeting_entry.get("1.0", "end").strip()
        meeting_date = self.view.meeting_date_entry.get()
        payment_status = self.view.payment_combo.get()
        payment_date = self.view.payment_date_entry.get()
        method = self.view.payment_method_combo.get()
        if method == "Payment Method":
            method = None

        total_str = self.view.total_entry.get()
        paid_str = self.view.paid_entry.get()

        total, err_total = self._parse_amount(total_str, "Total")
        paid, err_paid = self._parse_amount(paid_str, "Paid")

        errors = [Validators.validate_required(meeting, "Meeting")]

        if payment_status.lower() == "paid":
            errors.append(Validators.validate_date(meeting_date, "Meeting Date", allow_future=True))
            errors.append(Validators.validate_date(payment_date, "Payment Date", allow_future=False))
            if not paid_str.strip():
                paid = total
        else:
            if payment_date.strip():
                errors.append("Payment Date solo debe ingresarse si el estado es Paid.")
            errors.append(Validators.validate_date(meeting_date, "Meeting Date", allow_future=True))

        if err_total:
            errors.append(err_total)
        if err_paid:
            errors.append(err_paid)

        if paid > total:
            errors.append("Paid no puede ser mayor que Total.")

        errors = [e for e in errors if e]

        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return None

        return {
            "meeting": meeting,
            "meeting_date": meeting_date,
            "payment_status": payment_status,
            "payment_date": payment_date,
            "method": method,
            "total": total,
            "paid": paid,
        }

    def add_meeting(self, client_id: int) -> None:
        """
        Valida los datos y agrega una nueva reunión para el cliente seleccionado.
        """
        data = self._validate_meeting_data()
        if data is None:
            return

        try:
            new_id = self.model.add_meeting(
                client_id, data["meeting"], data["meeting_date"],
                data["payment_status"], data["total"], data["paid"],
                data["method"], data["payment_date"]
            )
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        messagebox.showinfo("Success", "Meeting added.")
        self.load_meetings(client_id)

    def update_meeting(self, client_id: int) -> None:
        """
        Valida y actualiza la reunión seleccionada del cliente.
        """
        meeting_id = self.view.get_selected_meeting_id()
        if not meeting_id:
            messagebox.showwarning("Warning", "Select a meeting to update.")
            return

        data = self._validate_meeting_data()
        if data is None:
            return

        try:
            self.model.update_meeting(
                meeting_id, data["meeting"], data["meeting_date"],
                data["payment_status"], data["total"], data["paid"],
                data["method"], data["payment_date"]
            )
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        messagebox.showinfo("Success", "Meeting updated.")
        self.load_meetings(client_id)

    def delete_meeting(self, client_id: int) -> None:
        """
        Elimina la reunión seleccionada tras confirmación del usuario.
        """
        meeting_id = self.view.get_selected_meeting_id()
        if not meeting_id:
            messagebox.showwarning("Warning", "Select a meeting to delete.")
            return

        selected = self.view.meetings_tree.selection()
        meeting_name = self.view.meetings_tree.item(selected[0])["values"][1]
        if not messagebox.askyesno("Confirm Delete",
                f"Delete meeting '{meeting_name}'?\nThis cannot be undone."):
            return

        try:
            self.model.delete_meeting(meeting_id)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        self.load_meetings(client_id)
