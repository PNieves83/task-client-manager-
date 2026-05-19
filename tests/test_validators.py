"""Tests unitarios para los validadores del modelo."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from model.validators import Validators


class TestValidateName:
    def test_nombre_valido(self):
        assert Validators.validate_name("Juan") is None

    def test_nombre_con_espacios(self):
        assert Validators.validate_name("María José") is None

    def test_nombre_con_tildes(self):
        assert Validators.validate_name("José") is None
        assert Validators.validate_name("Ángela") is None

    def test_nombre_con_ñ(self):
        assert Validators.validate_name("Muñoz") is None

    def test_nombre_vacio(self):
        assert Validators.validate_name("") is not None

    def test_nombre_solo_espacios(self):
        assert Validators.validate_name("   ") is not None

    def test_nombre_con_numeros(self):
        assert Validators.validate_name("Juan123") is not None

    def test_nombre_con_caracteres_especiales(self):
        assert Validators.validate_name("Juan@!") is not None

    def test_field_name_personalizado(self):
        err = Validators.validate_name("", "Username")
        assert "Username" in err


class TestValidatePhone:
    def test_telefono_valido_simple(self):
        assert Validators.validate_phone("123456") is None

    def test_telefono_con_codigo_pais(self):
        assert Validators.validate_phone("+54 11 5555-1234") is None

    def test_telefono_con_parentesis(self):
        assert Validators.validate_phone("(011) 5555-1234") is None

    def test_telefono_vacio(self):
        assert Validators.validate_phone("") is not None

    def test_telefono_demasiado_corto(self):
        assert Validators.validate_phone("12") is not None

    def test_telefono_con_letras(self):
        assert Validators.validate_phone("1234ABC") is not None


class TestValidateEmail:
    def test_email_valido(self):
        assert Validators.validate_email("test@mail.com") is None

    def test_email_con_puntos(self):
        assert Validators.validate_email("nombre.apellido@mail.com") is None

    def test_email_con_guiones(self):
        assert Validators.validate_email("test-user@mail.com") is None

    def test_email_sin_arroba(self):
        assert Validators.validate_email("testmail.com") is not None

    def test_email_sin_dominio(self):
        assert Validators.validate_email("test@") is not None

    def test_email_vacio(self):
        assert Validators.validate_email("") is not None

    def test_email_sin_punto(self):
        assert Validators.validate_email("test@mail") is not None


class TestValidateDate:
    def test_fecha_valida_dd_mm_yyyy(self):
        assert Validators.validate_date("15/03/2024") is None

    def test_fecha_valida_yyyy_mm_dd(self):
        assert Validators.validate_date("2024-03-15") is None

    def test_fecha_invalida(self):
        assert Validators.validate_date("99/99/9999") is not None

    def test_fecha_vacia(self):
        assert Validators.validate_date("") is not None

    def test_formato_incorrecto(self):
        assert Validators.validate_date("15-03-2024") is not None

    def test_fecha_anterior_1900(self):
        assert Validators.validate_date("15/03/1800") is not None

    def test_fecha_futura_no_permitida(self):
        assert Validators.validate_date("31/12/2099", allow_future=False) is not None


class TestValidateRequired:
    def test_campo_lleno(self):
        assert Validators.validate_required("texto", "Campo") is None

    def test_campo_vacio(self):
        assert Validators.validate_required("", "Campo") is not None

    def test_campo_solo_espacios(self):
        assert Validators.validate_required("   ", "Campo") is not None

    def test_mensaje_contiene_nombre_campo(self):
        err = Validators.validate_required("", "Email")
        assert "Email" in err


class TestValidateAmount:
    def test_monto_entero(self):
        assert Validators.validate_amount("100") is None

    def test_monto_decimal_punto(self):
        assert Validators.validate_amount("100.50") is None

    def test_monto_decimal_coma(self):
        assert Validators.validate_amount("100,50") is None

    def test_monto_vacio(self):
        assert Validators.validate_amount("") is None

    def test_monto_negativo(self):
        assert Validators.validate_amount("-50") is not None

    def test_monto_no_numerico(self):
        assert Validators.validate_amount("abc") is not None

    def test_monto_cero(self):
        assert Validators.validate_amount("0") is None
