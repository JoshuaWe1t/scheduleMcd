import datetime

from sqlalchemy.orm import sessionmaker

import models
from scheduleMcd.backend.tests.engine import engine

Session = sessionmaker()

def check_user_exists(user: str) -> bool:
    """
    Проверка, что пользователь существует в системе

    Args:
        user (str): Код пользователя
    
    Return:
        Признак существования сотрудника в БД
    """
    session = Session(bind=engine)
    try:
        user_code = session.query(models.Emploeeys.code).filter(
            models.Emploeeys.code == user).first()
        session.commit()
    except:
        session.rollback()
        print('Rolled back')
        raise
    finally:
        session.close()

    return bool(user_code)


def autorization(user_data: dict) -> dict:
    """
    Проверка корректности ввода учетных данных пользователя

    Args:
        user (dict): {"usercode": str, "password": str}
    
    Return:
        dict: {"status": bool, "user_data": dict}
    """
    user_db_data = get_user_data(user_data.get("usercode"))
    if user_db_data.get("Error"):
        return {
                "status": False,
                "user_data": {}
                }
    
    if user_db_data.get("password") == user_data.get("password"):
        return {
                "status": True,
                "user_data": user_db_data
                }


def get_user_data(user: str) -> dict:
    """
    Получение данных пользователя

    Args:
        user (str): Код пользователя

    Return:
        Если пользователь существует, то возвращается словарь с актуальными данными пользователя. 
        {
            "code": "000000",
            "password": F42ACBD5644,
            "id_specialization": 0,
            "id_department": 27000
        }
        Иначе возвращается словарь {"Error": "User <user_code> does not exist"}
    """
    if check_user_exists(user):
        session = Session(bind=engine)
        try:
            query = session.query(models.Emploeeys.code, 
                              models.Emploeeys.pswrd,
                              models.Emploeeys.id_specialization,
                              models.Emploeeys.id_department
                            ).filter(models.Emploeeys.code == user).first()
            user_data = {
                "code": query[0],
                "password": query[1],
                "id_specialization": query[2],
                "id_department": query[3]
            }
            session.commit()
        except:
            session.rollback()
            print('Rolled back')
            raise
        finally:
            session.close()

        return user_data

    return {"Error": 404}


def add_schedule_data(schedule_data: dict):
    """
    Добавление расписания сотрудника в таблицу фактов

    Args:
        user (str): Код пользователя
    """
    session = Session(bind=engine)
    try:
        # бизнес-логика
        fct_schedule = models.FctSchedule(
            code_emploeey=schedule_data["code"],
            mon=schedule_data["mon"],
            tue=schedule_data["tue"],
            wed=schedule_data["wed"],
            thu=schedule_data["thu"],
            fri=schedule_data["fri"],
            sat=schedule_data["sat"],
            sun=schedule_data["sun"],
            record_dt=schedule_data["dt"],
            week_num=schedule_data["week_num"],
            week_start_date=schedule_data["week_start_date"],
            status=schedule_data["status"]
        )
        session.add(fct_schedule)
        session.commit()
        print(f'В базу записана строка {fct_schedule.id}')
    except:
        session.rollback()
        print('Rolled back')
        raise
    finally:
        session.close()

def get_three_records_for_user(user: str): 
    """
    Получение последних трех записей расписания сотрудника

    Args:
        user (str): Код пользователя
    """
    session = Session(bind=engine)
    try:
        schedule = session.query(models.FctSchedule)\
            .filter(models.FctSchedule.code_emploeey == user)\
            .order_by(models.FctSchedule.id)\
            .limit(3)\
            .all()
        session.commit()
        # Преобразуем в словари
        result = []
        for obj in schedule:
            result.append({
                "mon": obj.mon,
                "tue": obj.tue,
                "wed": obj.wed,
                "thu": obj.thu,
                "fri": obj.fri,
                "sat": obj.sat,
                "sun": obj.sun,
                "status": obj.status,
                "date": obj.record_dt.isoformat()
            })
        print(result)
    except:
        session.rollback()
        print('Rolled back')
        raise
    finally:
        session.close()

    return result


def create_list_of_schedules(l_data: list):
    """
    Добавление в список унифицированные данные по расписаниям сотрудника

    Args:
        l_data (list): Список данных по расписанию
    Return:
        result (list[dict]): Список словарей с данными по расписаниям
    """
    result = []
    for t_elm in l_data:
        print(t_elm)
        item = {
            "code_emploeey": t_elm[0],
            "first_name": t_elm[1],
            "mon": t_elm[2],
            "tue": t_elm[3],
            "wed": t_elm[4],
            "thu": t_elm[5],
            "fri": t_elm[6],
            "sat": t_elm[7],
            "sun": t_elm[8],
            "week_start_date": str(t_elm[9])
        }
        result.append(item)
    return result


def get_employees_schedules(manager_data: dict):
    """
    Получение расписаний сотрудников департамента для менеджера

    Args:
        manager_data (dict): Данные менеджера

    Return:
        schedules (list): Список объектов расписаний сотрудников
    """
    session = Session(bind=engine)
    try:
        data = session.query(models.FctSchedule.code_emploeey,
                             models.Emploeeys.first_name,
                             models.FctSchedule.mon,
                             models.FctSchedule.tue,
                             models.FctSchedule.wed,
                             models.FctSchedule.thu,
                             models.FctSchedule.fri,
                             models.FctSchedule.sat,
                             models.FctSchedule.sun,
                             models.FctSchedule.week_start_date)\
            .join(models.Emploeeys, 
                  models.Emploeeys.code == models.FctSchedule.code_emploeey)\
            .filter(models.Emploeeys.id_department == manager_data.get("id_department"),
                    models.FctSchedule.status == "wait")\
            .all()

        session.commit()
        print(create_list_of_schedules(data))
        return create_list_of_schedules(data)
    except:
        session.rollback()
        print('Rolled back')
        raise
    finally:
        session.close()


def T1(code: str, status="reject"):
    """
    """
    from sqlalchemy import func
    session = Session(bind=engine)
    try:
        max_dt = session.query(func.max(models.FctSchedule.week_start_date))\
            .filter(models.FctSchedule.status == "wait", 
                    models.FctSchedule.code_emploeey == code)\
            .first()
        print(max_dt)
        data = session.query(models.FctSchedule)\
            .filter(models.FctSchedule.status == "wait", 
                    models.FctSchedule.code_emploeey == code,
                    models.FctSchedule.week_start_date == max_dt)\
            .first()
        print(data)
        data.status = status
        session.commit()
    except:
        session.rollback()
        print('Rolled back')
        raise
    finally:
        session.close()

T1("400000")

d_schedule = [
    {
        "code": "400000",
        "mon": "07:00-16:00",
        "tue": "07:00-15:00",
        "wed": "Day off",
        "thu": "Day off",
        "fri": "16:00-23:00",
        "sat": "16:00-23:00",
        "sun": "12:00-18:00",
        "dt": "2025-05-28",
        "week_num": 25,
        "week_start_date": "2025-05-23",
        "status": "approved"
    },
    {
        "code": "400000",
        "mon": "Day off",
        "tue": "07:00-15:00",
        "wed": "Day off",
        "thu": "Day off",
        "fri": "10:00-23:00",
        "sat": "10:00-23:00",
        "sun": "12:00-16:00",
        "dt": "2025-07-03",
        "week_num": 26,
        "week_start_date": "2025-05-30",
        "status": "wait"
    },
    {
        "code": "200000",
        "mon": "08:00-16:00",
        "tue": "09:00-15:00",
        "wed": "Day off",
        "thu": "Day off",
        "fri": "18:00-23:00",
        "sat": "07:00-23:00",
        "sun": "08:00-18:00",
        "dt": "2025-05-28",
        "week_num": 25,
        "week_start_date": "2025-05-23",
        "status": "reject"
    },
    {
        "code": "200000",
        "mon": "07:00-16:00",
        "tue": "07:00-15:00",
        "wed": "Day off",
        "thu": "18:00-23:00",
        "fri": "18:00-23:00",
        "sat": "07:00-23:00",
        "sun": "Day off",
        "dt": "2025-05-28",
        "week_num": 25,
        "week_start_date": "2025-05-23",
        "status": "approved"
    },
    {
        "code": "200000",
        "mon": "Day off",
        "tue": "07:00-15:00",
        "wed": "Day off",
        "thu": "Day off",
        "fri": "10:00-23:00",
        "sat": "10:00-23:00",
        "sun": "12:00-16:00",
        "dt": "2025-07-03",
        "week_num": 26,
        "week_start_date": "2025-05-30",
        "status": "wait"
    },
]
# add_schedule_data(d_schedule)
# get_three_records_for_user("400000")

# for obj in d_schedule:
#     add_schedule_data(obj)

# print(get_user_data("100000"))
# print(get_user_data("400000"))

manager_data = {
    "code": "100000",
    "password": "SQunFR",
    "id_specialization": 9,
    "id_department": 27000
}

# get_employees_schedules(manager_data)

[
    {'code_emploeey': '400000', 'mon': 'Day off', 'tue': '07:00-15:00', 'wed': 'Day off', 'thu': 'Day off', 'fri': '10:00-23:00', 'sat': '10:00-23:00', 'sun': '12:00-16:00', 'week_start_date': '2025-05-30'}, 
    {'code_emploeey': '200000', 'mon': 'Day off', 'tue': '07:00-15:00', 'wed': 'Day off', 'thu': 'Day off', 'fri': '10:00-23:00', 'sat': '10:00-23:00', 'sun': '12:00-16:00', 'week_start_date': '2025-05-30'}, 
    {'code_emploeey': '400000', 'mon': 'Day off', 'tue': '07:00-15:00', 'wed': 'Day off', 'thu': 'Day off', 'fri': '10:00-23:00', 'sat': '10:00-23:00', 'sun': '12:00-16:00', 'week_start_date': '2025-05-30'}, 
    {'code_emploeey': '200000', 'mon': 'Day off', 'tue': '07:00-15:00', 'wed': 'Day off', 'thu': 'Day off', 'fri': '10:00-23:00', 'sat': '10:00-23:00', 'sun': '12:00-16:00', 'week_start_date': '2025-05-30'}
]

