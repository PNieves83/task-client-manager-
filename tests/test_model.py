"""Tests unitarios para la capa de modelo (CRUD)."""
import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from model.database import create_connection, create_tables
from model.model import Model


@pytest.fixture
def temp_db():
    """Crea una base de datos temporal para las pruebas."""
    tmpdir = tempfile.mkdtemp()
    db_path = os.path.join(tmpdir, "test.db")
    from model import database
    original_db_path = database.DB_PATH
    database.DB_PATH = db_path
    create_tables()
    yield db_path
    database.DB_PATH = original_db_path
    import shutil
    shutil.rmtree(tmpdir, ignore_errors=True)


class TestModel:
    def test_add_client(self, temp_db):
        model = Model()
        client_id = model.add_client("Juan", "Pérez", "juan@mail.com", "123456789",
                                     "ACME", "Client", "Website", "Email")
        assert client_id > 0

    def test_get_clients(self, temp_db):
        model = Model()
        model.add_client("Ana", "García", "ana@mail.com", "987654321",
                         "Corp", "VIP", "Referral", "Phone")
        clients = model.get_clients()
        assert len(clients) == 1
        assert clients[0][1] == "Ana"

    def test_update_client(self, temp_db):
        model = Model()
        cid = model.add_client("Carlos", "López", "carlos@mail.com", "5551234",
                               "Startup", "Lead", "Instagram", "WhatsApp")
        model.update_client(cid, "Carlos", "López", "carlos.new@mail.com", "5555678",
                            "Startup", "Client", "Instagram", "Email")
        clients = model.get_clients()
        assert clients[0][3] == "carlos.new@mail.com"

    def test_delete_client_deletes_tasks(self, temp_db):
        model = Model()
        cid = model.add_client("Test", "User", "test@mail.com", "111111",
                               "", "Client", "Website", None)
        model.add_task(cid, "Tarea de prueba", "Pending", "01/01/2026", "15/01/2026")
        model.delete_client(cid)
        assert len(model.get_clients()) == 0
        assert len(model.get_tasks_by_client(cid)) == 0

    def test_add_task(self, temp_db):
        model = Model()
        cid = model.add_client("Task", "Client", "tc@mail.com", "222222",
                               "", "Client", "Website", None)
        tid = model.add_task(cid, "Completar informe", "In Progress", "10/05/2026", "20/05/2026")
        assert tid > 0
        tasks = model.get_tasks_by_client(cid)
        assert len(tasks) == 1
        assert tasks[0][1] == "Completar informe"

    def test_update_task(self, temp_db):
        model = Model()
        cid = model.add_client("UT", "Client", "utc@mail.com", "333333",
                               "", "Client", "Website", None)
        tid = model.add_task(cid, "Diseñar logo", "Pending", "01/06/2026", "10/06/2026")
        model.update_task(tid, "Diseñar logo v2", "Completed", "01/06/2026", "08/06/2026")
        tasks = model.get_tasks_by_client(cid)
        assert tasks[0][2] == "Completed"

    def test_delete_task(self, temp_db):
        model = Model()
        cid = model.add_client("DT", "Client", "dtc@mail.com", "444444",
                               "", "Client", "Website", None)
        tid = model.add_task(cid, "Tarea a eliminar", "Pending", "01/07/2026", "15/07/2026")
        model.delete_task(tid)
        assert len(model.get_tasks_by_client(cid)) == 0

    def test_add_meeting(self, temp_db):
        model = Model()
        cid = model.add_client("Meeting", "Client", "mc@mail.com", "555555",
                               "", "Client", "Website", None)
        mid = model.add_meeting(cid, "Revisión semanal", "15/05/2026",
                                "Paid", 500.0, 500.0, "Cash", "15/05/2026")
        assert mid > 0
        meetings = model.get_meetings_by_client(cid)
        assert len(meetings) == 1

    def test_update_meeting(self, temp_db):
        model = Model()
        cid = model.add_client("UM", "Client", "umc@mail.com", "666666",
                               "", "Client", "Website", None)
        mid = model.add_meeting(cid, "Sesión inicial", "20/05/2026",
                                "Unpaid", 1000.0, 0.0, None, "")
        model.update_meeting(mid, "Sesión inicial", "20/05/2026",
                             "Partially Paid", 1000.0, 300.0, "Credit Card", "22/05/2026")
        meetings = model.get_meetings_by_client(cid)
        assert meetings[0][3] == "Partially Paid"

    def test_delete_meeting(self, temp_db):
        model = Model()
        cid = model.add_client("DM", "Client", "dmc@mail.com", "777777",
                               "", "Client", "Website", None)
        mid = model.add_meeting(cid, "Reunión a eliminar", "25/05/2026",
                                "Pending", 0.0, 0.0, None, "")
        model.delete_meeting(mid)
        assert len(model.get_meetings_by_client(cid)) == 0

    def test_get_clients_empty(self, temp_db):
        model = Model()
        assert model.get_clients() == []

    def test_get_tasks_no_client(self, temp_db):
        model = Model()
        assert model.get_tasks_by_client(999) == []

    def test_get_meetings_no_client(self, temp_db):
        model = Model()
        assert model.get_meetings_by_client(999) == []
