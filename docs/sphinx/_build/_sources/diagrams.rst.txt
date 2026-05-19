Diagramas de arquitectura
=========================

Diagrama MVC
------------

El proyecto sigue el patrón **Modelo-Vista-Controlador (MVC)**.
El siguiente diagrama muestra las relaciones entre las clases
principales:

.. mermaid::

   classDiagram
       class Controller {
           +set_view(view)
           +add_client()
           +update_client()
           +delete_client()
           +load_clients()
           +add_task()
           +update_task()
           +delete_task()
           +load_tasks()
           +add_meeting()
           +update_meeting()
           +delete_meeting()
           +load_meetings()
       }

       class TaskView {
           +update_clients_table()
           +update_tasks_table()
           +update_meetings_table()
           +get_selected_client_id()
           +get_selected_task_id()
           +get_selected_meeting_id()
       }

       class Model {
           +add_client()
           +get_clients()
           +update_client()
           +delete_client()
           +add_task()
           +get_tasks_by_client()
           +update_task()
           +delete_task()
           +add_meeting()
           +get_meetings_by_client()
           +update_meeting()
           +delete_meeting()
       }

       class Validators {
           <<static>>
           +validate_name()
           +validate_email()
           +validate_phone()
           +validate_date()
           +validate_required()
           +validate_amount()
       }

       Controller --> Model : usa
       Controller --> TaskView : controla
       TaskView --> Controller : llama
       Controller --> Validators : valida

Diagrama de la base de datos
----------------------------

La base de datos SQLite está compuesta por tres tablas principales
relacionadas mediante claves foráneas:

.. mermaid::

   erDiagram
       CLIENTS {
           int id PK
           text name
           text last_name
           text email
           text phone
           text company
           text category
           text source
           text preferred_method
       }

       TASKS {
           int id PK
           int client_id FK
           text task
           text task_status
           text start_date
           text deadline
       }

       MEETINGS {
           int id PK
           int client_id FK
           text meeting
           text meeting_date
           text payment_status
           real total
           real paid
           text method
           text payment_date
       }

       CLIENTS ||--o{ TASKS : tiene
       CLIENTS ||--o{ MEETINGS : tiene
