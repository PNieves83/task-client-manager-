# model/validators.py

import re
from datetime import datetime
from typing import Optional
from utils.config import FORMATS


class Validators:
    """
    Colección de validadores estáticos para campos del formulario.

    Cada método recibe un valor y retorna None si es válido o un
    mensaje de error en caso contrario.
    """
    # VALIDACIÓN DE NOMBRES
    @staticmethod
    def validate_name(value: str, field_name: str = "Name") -> Optional[str]:
        """Valida que el campo tenga solo letras y espacios."""
        if not value or not value.strip():
            return f"El campo '{field_name}' no puede estar vacío."

        pattern = r"^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$"
        if not re.match(pattern, value):
            return f"El campo '{field_name}' solo puede contener letras y espacios."

        return None

    # VALIDACIÓN DE TELÉFONO
    @staticmethod
    def validate_phone(value: str, field_name: str = "Phone") -> Optional[str]:
        """Valida formato de teléfono."""
        if not value or not value.strip():
            return f"El campo '{field_name}' no puede estar vacío."

        pattern = r"^[0-9+\-() ]{6,20}$"
        if not re.match(pattern, value):
            return f"El campo '{field_name}' contiene un formato de teléfono inválido."

        return None

    # VALIDACIÓN DE EMAIL
    @staticmethod
    def validate_email(value: str, field_name: str = "Email") -> Optional[str]:
        """Valida formato de email."""
        if not value or not value.strip():
            return f"El campo '{field_name}' no puede estar vacío."

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, value):
            return f"El campo '{field_name}' no tiene un formato de email válido."

        return None

    # VALIDACIÓN DE FECHAS (Opción C)
    @staticmethod
    def validate_date(value: str, field_name: str = "Date", allow_future: bool = True) -> Optional[str]:
        """
        Valida formato de fecha según FORMATS["date"] (dd/mm/yyyy)
        y también acepta yyyy-mm-dd.

        allow_future:
            True  → se permiten fechas futuras (Meetings, Tasks)
            False → NO se permiten fechas futuras (Payment Date)
        """
        if not value or not value.strip():
            return f"El campo '{field_name}' no puede estar vacío."

        # Formatos permitidos
        allowed_formats = [
            FORMATS["date"],   # dd/mm/yyyy
            "%Y-%m-%d"         # yyyy-mm-dd
        ]

        # Validar contra patrones
        patterns = [
            r"^\d{2}/\d{2}/\d{4}$",
            r"^\d{4}-\d{2}-\d{2}$"
        ]

        if not any(re.match(p, value) for p in patterns):
            return f"El campo '{field_name}' debe tener formato dd/mm/yyyy o yyyy-mm-dd."

        # Validar fecha real
        date_obj = None
        for fmt in allowed_formats:
            try:
                date_obj = datetime.strptime(value, fmt)
                break
            except ValueError:
                continue

        if date_obj is None:
            return f"El campo '{field_name}' no contiene una fecha válida."

        # Año mínimo
        if date_obj.year < 1900:
            return f"El campo '{field_name}' no puede ser anterior al año 1900."

        # Fechas futuras según opción C
        if not allow_future and date_obj > datetime.now():
            return f"El campo '{field_name}' no puede ser una fecha futura."

        return None

    # VALIDACIÓN DE CAMPOS OBLIGATORIOS
    @staticmethod
    def validate_required(value: str, field_name: str) -> Optional[str]:
        """Valida que el campo no esté vacío."""
        if not value or not value.strip():
            return f"El campo '{field_name}' no puede estar vacío."
        return None

    # VALIDACIÓN DE MONTOS
    @staticmethod
    def validate_amount(value: str, field_name: str = "Amount") -> Optional[str]:
        """
        Valida que el monto sea numérico y no negativo.
        Acepta coma o punto.
        """
        if not value or not value.strip():
            return None  # vacío se maneja en el controlador

        try:
            num = float(value.replace(",", "."))
            if num < 0:
                return f"El campo '{field_name}' no puede ser negativo."
            return None
        except ValueError:
            return f"El campo '{field_name}' debe ser numérico."
