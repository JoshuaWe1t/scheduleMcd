from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

import models
from scheduleMcd.backend.tests.engine import engine

Session = sessionmaker()

specialization_data = [
    {"id": 0, "name": 'K', "description": 'Кухонный работник'},
    {"id": 1, "name": 'C', "description": 'Работник бара'},
    {"id": 2, "name": 'DT', "description": 'Работник автораздачи'},
    {"id": 3, "name": 'NTR', "description": 'Работник ночной смены подготовки предприятия'},
    {"id": 4, "name": 'T', "description": 'Работник разноса заказов в предприятии'},
    {"id": 5, "name": 'U', "description": 'Универсальный работник на каждую из роль, исключая NTR'},
    {"id": 6, "name": 'ELT', "description": 'Работник стойки администратора'},
    {"id": 7, "name": 'K|C', "description": 'Работник кухни и бара'},
    {"id": 8, "name": 'C|DT', "description": 'Работник бара и автораздачи'},
    {"id": 9, "name": 'MNG', "description": 'Менеджер'}
]

emploeeys_data = [
    {"id": 202, "code": "100000", "first_name": "Maria", "last_name": "Ivanova", "middle_name": None, "id_specialization": 9, "pswrd": "SQunFR", "id_department": 27000},
    {"id": 102, "code": "400000", "first_name": "Nick", "last_name": "Middle", "middle_name": "Von", "id_specialization": 1, "pswrd": "jM3I9d", "id_department": 27000},
    {"id": 17, "code": "200000", "first_name": "Nil", "last_name": "Van", "middle_name": None, "id_specialization": 4, "pswrd": "zioHAY", "id_department": 27000}
]

department_data = [
    {"id": 27000, "name": "Мидгард"},
    {"id": 19800, "name": "Барса"}
]

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session(bind=engine)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def added_data_into_model(data: list, model: object):
    with session_scope() as session:
        specialization = [model(**item) for item in data]
        session.add_all(specialization)
        print(f'Записано в базу {session.query(model).count()} строк')

# added_data_into_model(specialization_data, models.Specialization)
# added_data_into_model(department_data, models.Department)
added_data_into_model(emploeeys_data, models.Emploeeys)