from typing import Any, Optional
from model.database import create_connection


class Model:
    """
    Capa de acceso a datos. Ejecuta operaciones CRUD sobre la base de datos.

    Todas las consultas pasan por el método interno _execute que maneja
    la conexión, cursor, commit, rollback y cierre automáticamente.
    """

    #   EJECUTOR SQL ROBUSTO
    def _execute(self, query: str, params: tuple = (), fetch: bool = False, fetchone: bool = False, return_id: bool = False) -> Any:
        """
        Ejecuta una consulta SQL con manejo de errores.
        return_id=True → devuelve el ID recién creado (SQLite RETURNING id)
        """
        conn = create_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, params)

            # Obtener ID recién creado
            if return_id:
                new_id = cursor.fetchone()[0]
                conn.commit()
                conn.close()
                return new_id

            # Fetch múltiple
            if fetch:
                result = cursor.fetchall()
                conn.commit()
                conn.close()
                return result

            # Fetch uno
            if fetchone:
                result = cursor.fetchone()
                conn.commit()
                conn.close()
                return result

            conn.commit()
            conn.close()
            return None

        except Exception as e:
            conn.rollback()
            conn.close()
            raise e

    #   CLIENTES
    def add_client(self, name: str, last_name: str, email: str, phone: str, company: str, category: str, source: str, preferred_method: Optional[str]) -> int:
        """
        Inserta un nuevo cliente en la base de datos.

        Returns:
            int: ID del cliente recién creado.
        """
        return self._execute(
            """
            INSERT INTO clients (name, last_name, email, phone, company, category, source, preferred_method)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING id
            """,
            (name, last_name, email, phone, company, category, source, preferred_method),
            return_id=True
        )

    def get_clients(self) -> list:
        """
        Obtiene todos los clientes ordenados por nombre.

        Returns:
            list[tuple]: Lista de clientes con sus datos completos.
        """
        return self._execute(
            """
            SELECT id, name, last_name, email, phone, preferred_method, company, category, source
            FROM clients
            ORDER BY name ASC
            """,
            fetch=True
        )

    def update_client(self, client_id: int, name: str, last_name: str, email: str, phone: str, company: str, category: str, source: str, preferred_method: Optional[str]) -> None:
        """
        Actualiza los datos de un cliente existente."""
        self._execute(
            """
            UPDATE clients
            SET name=?, last_name=?, email=?, phone=?, company=?, category=?, source=?, preferred_method=?
            WHERE id=?
            """,
            (name, last_name, email, phone, company, category, source, preferred_method, client_id)
        )

    def delete_client(self, client_id: int) -> None:
        """
        Elimina un cliente y sus tareas y reuniones asociadas por ID.
        """
        self._execute("DELETE FROM tasks WHERE client_id=?", (client_id,))
        self._execute("DELETE FROM meetings WHERE client_id=?", (client_id,))
        self._execute("DELETE FROM clients WHERE id=?", (client_id,))

    #   TASKS
    def add_task(self, client_id: int, task: str, task_status: str, start_date: str, deadline: str) -> int:
        """
        Inserta una nueva tarea para un cliente.

        Returns:
            int: ID de la tarea recién creada.
        """
        return self._execute(
            """
            INSERT INTO tasks (client_id, task, task_status, start_date, deadline)
            VALUES (?, ?, ?, ?, ?)
            RETURNING id
            """,
            (client_id, task, task_status, start_date, deadline),
            return_id=True
        )

    def get_tasks_by_client(self, client_id: int) -> list:
        """
        Obtiene todas las tareas de un cliente ordenadas por fecha de inicio.

        Returns:
            list[tuple]: Lista de tareas del cliente.
        """
        return self._execute(
            """
            SELECT id, task, task_status, start_date, deadline
            FROM tasks
            WHERE client_id=?
            ORDER BY 
                CASE WHEN start_date = '' OR start_date IS NULL THEN 1 ELSE 0 END,
                start_date ASC
            """,
            (client_id,),
            fetch=True
        )

    def update_task(self, task_id: int, task: str, task_status: str, start_date: str, deadline: str) -> None:
        """
        Actualiza los datos de una tarea existente.
        """
        self._execute(
            """
            UPDATE tasks
            SET task=?, task_status=?, start_date=?, deadline=?
            WHERE id=?
            """,
            (task, task_status, start_date, deadline, task_id)
        )

    def delete_task(self, task_id: int) -> None:
        """
        Elimina una tarea por su ID.
        """
        self._execute("DELETE FROM tasks WHERE id=?", (task_id,))

    #   MEETINGS
    def add_meeting(self, client_id: int, meeting: str, meeting_date: str, payment_status: str, total: float, paid: float, method: Optional[str], payment_date: str) -> int:
        """
        Inserta una nueva reunión para un cliente.

        Returns:
            int: ID de la reunión recién creada.
        """
        return self._execute(
            """
            INSERT INTO meetings (client_id, meeting, meeting_date, payment_status, total, paid, method, payment_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING id
            """,
            (client_id, meeting, meeting_date, payment_status, total, paid, method, payment_date),
            return_id=True
        )

    def get_meetings_by_client(self, client_id: int) -> list:
        """
        Obtiene todas las reuniones de un cliente ordenadas por fecha.

        Returns:
            list[tuple]: Lista de reuniones del cliente.
        """
        return self._execute(
            """
            SELECT id, meeting, meeting_date, payment_status, total, paid, method, payment_date
            FROM meetings
            WHERE client_id=?
            ORDER BY 
                CASE WHEN meeting_date = '' OR meeting_date IS NULL THEN 1 ELSE 0 END,
                meeting_date ASC
            """,
            (client_id,),
            fetch=True
        )

    def update_meeting(self, meeting_id: int, meeting: str, meeting_date: str, payment_status: str, total: float, paid: float, method: Optional[str], payment_date: str) -> None:
        """
        Actualiza los datos de una reunión existente.
        """
        self._execute(
            """
            UPDATE meetings
            SET meeting=?, meeting_date=?, payment_status=?, total=?, paid=?, method=?, payment_date=?
            WHERE id=?
            """,
            (meeting, meeting_date, payment_status, total, paid, method, payment_date, meeting_id)
        )

    def delete_meeting(self, meeting_id: int) -> None:
        """
        Elimina una reunión por su ID.
        """
        self._execute("DELETE FROM meetings WHERE id=?", (meeting_id,))
