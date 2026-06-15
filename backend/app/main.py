from urllib.parse import urlsplit
import datetime
from datetime import date

import sqlalchemy as sa
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required

from scheduleMcd.backend.config import VERSION, DEVELOPERS
from scheduleMcd.backend.app import app, db
from scheduleMcd.backend.app.forms import LoginForm, LogoutBtn, ScheduleForm, ScheduleMng
from scheduleMcd.backend.app.models import Emploeeys, FctSchedule


ROLE_REDIRECTS = {
    'emp': 'view_employee', 
    'mng': 'view_manager'   
}

# Вспомогательная функция для перенаправления по роли
def redirect_to_role_page(role):
    endpoint = ROLE_REDIRECTS.get(role, False)
    return redirect(url_for(endpoint))


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect_to_role_page(current_user.role)
    return redirect(url_for('login'))  


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(Emploeeys).where(
                Emploeeys.code == form.username.data
            )
        )
        
        if user and user.check_password(form.password.data):
            login_user(user)
            print(f"After login, current_user: {current_user}, is_authenticated: {current_user.is_authenticated}")  # Должно быть True
            # Проверяем, куда мы перенаправляем
            print(f"Redirecting to: {ROLE_REDIRECTS.get(user.role)}")
            return redirect_to_role_page(user.role)
        else:
            flash("Неверное имя пользователя или пароль", "danger")
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/employee", methods=['GET', 'POST'])
@login_required
def view_employee():
    print(f"Authenticated: {current_user.__dir__}")
    print(current_user.code)
    form_logout = LogoutBtn()
    form_schedule = ScheduleForm()
    path_to_icon = "../static/images/united-states-of-america.png"
    about = {}
    about['title'] = 'About Service'
    about["version"] = VERSION
    about['developers'] = DEVELOPERS.split(",")
    about["copyright"] = "All rights reserved"
    introduction = {}
    introduction["title"] = "Introduction"
    introduction["content"] = "Lorem ipsum odor amet, consectetuer adipiscing elit."
    context = {
        "about" : about,
        "introduction": introduction
    }
    employee_data = get_records_user(current_user.code)
    table_context = {
        "match_data": {
            1: "mon",
            2: "tue",
            3: "wed",
            4: "thu",
            5: "fri",
            6: "sat",
            7: "sun",
            8: "status",
            9: "date"
        },
        "ROW": len(employee_data),
        "COLUMN": 9,
        "user_data": employee_data
    }
    if form_schedule.validate_on_submit():
        print(42)
        user_schedule = {
            "code": current_user.code,
            "mon": form_schedule.mon.data if form_schedule.mon.data != '' else "Day off",
            "tue": form_schedule.tue.data if form_schedule.tue.data != '' else "Day off",
            "wed": form_schedule.wed.data if form_schedule.wed.data != '' else "Day off",
            "thu": form_schedule.thu.data if form_schedule.thu.data != '' else "Day off",
            "fri": form_schedule.fri.data if form_schedule.fri.data != '' else "Day off",
            "sat": form_schedule.sat.data if form_schedule.sat.data != '' else "Day off",
            "sun": form_schedule.sun.data if form_schedule.sun.data != '' else "Day off",
            "dt": date.today(),
            "week_num": date.today().isocalendar()[1],
            "week_start_date": start_of_week(date.today()),
            "status": "wait"
        }
        print(user_schedule)
        add_schedule_data(user_schedule)
    else:
        print("Error validation form")

    return render_template("employee.html", 
                           context=context, 
                           form_logout=form_logout, 
                           path_to_icon=path_to_icon, 
                           form_schedule=form_schedule,
                           table=table_context)


def add_schedule_data(schedule_data: dict):
    """
    Добавление расписания сотрудника в таблицу фактов

    Args:
        user (str): Код пользователя
    """
    session = db.session
    try:
        # бизнес-логика
        fct_schedule = FctSchedule(
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
    # finally:
    #     session.close()


def get_records_user(user: str, cnt_record=3) -> list: 
    """
    Получение записей расписания сотрудника

    Args:
        user (str): Код пользователя
        cnt_record (int): Количество получаемых записей

    Return:
        result (list[dict]): Список словарей с данными по расписанию пользователя
        [
            {
                "mon": "00:00-07:00",
                "tue": "00:00-07:00",
                "wed": "00:00-07:00",
                "thu": "00:00-07:00",
                "fri": "00:00-07:00",
                "sat": "00:00-07:00",
                "sun": "00:00-07:00",
                "status": "wait",
                "date": "1970-01-01"
            },
        ]
    """
    session = db.session
    try:
        schedule = session.query(FctSchedule)\
            .filter(FctSchedule.code_emploeey == user)\
            .order_by(FctSchedule.id)\
            .limit(cnt_record)\
            .all()
        session.commit()
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
        # print(result)
    except:
        session.rollback()
        print('Rolled back')
        raise
    return result


def start_of_week(date_obj):
    """
    Возвращает начало недели для заданной даты.
    По умолчанию начало недели - понедельник.
    """
    weekday = date_obj.weekday()
    start_of_week_date = date_obj - datetime.timedelta(days=weekday)
    return start_of_week_date


@app.route("/manager", methods=['GET', 'POST'])
@login_required
def view_manager():
    form_logout = LogoutBtn()
    path_to_icon = "../static/images/united-states-of-america.png"
    about = {}
    about['title'] = 'About Service'
    about["version"] = VERSION
    about['developers'] = DEVELOPERS.split(",")
    about["copyright"] = "All rights reserved"
    introduction = {}
    introduction["title"] = "Introduction"
    introduction["content"] = "Lorem ipsum odor amet, consectetuer adipiscing elit."
    context = {
        "about" : about,
        "introduction": introduction
    }

    manager_name = f"{current_user.first_name} {current_user.last_name}"
    # users_shedule = get_employees_schedules(current_user.id_department)
    # cnt_records = len(users_shedule)

    form_schedule_mng = ScheduleMng()

    if form_schedule_mng.validate_on_submit():
        user_code = form_schedule_mng.code_user.data 
        if form_schedule_mng.approved.data:
            update_employee_status(user_code, "approved")
        elif form_schedule_mng.reject.data:
            update_employee_status(user_code, "reject")
        else:
            print(0)

    users_shedule = get_employees_schedules(current_user.id_department)
    cnt_records = len(users_shedule)

    return render_template("manager.html", 
                           context=context, 
                           form_logout=form_logout, 
                           path_to_icon=path_to_icon,
                           manager_name=manager_name,
                           cnt_records=cnt_records,
                           users_shedule=users_shedule,
                           form_schedule_mng=form_schedule_mng)


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
            "code_employee": t_elm[0],
            "first_name": t_elm[1],
            "mon": t_elm[2],
            "tue": t_elm[3],
            "wed": t_elm[4],
            "thu": t_elm[5],
            "fri": t_elm[6],
            "sat": t_elm[7],
            "sun": t_elm[8],
            "week_start_date": str(t_elm[9]),
            "id": t_elm[10]
        }
        count_day_off = list(item.values()).count('Day off')
        item['cnt_day_off'] = count_day_off
        result.append(item)
    return result


def get_employees_schedules(id_department: int):
    """
    Получение расписаний сотрудников департамента для менеджера

    Args:
        id_department (int): Номер департамента

    Return:
        schedules (list): Список объектов расписаний сотрудников
    """
    session = db.session
    try:
        data = session.query(FctSchedule.code_emploeey,
                             Emploeeys.first_name,
                             FctSchedule.mon,
                             FctSchedule.tue,
                             FctSchedule.wed,
                             FctSchedule.thu,
                             FctSchedule.fri,
                             FctSchedule.sat,
                             FctSchedule.sun,
                             FctSchedule.week_start_date,
                             Emploeeys.id)\
            .join(Emploeeys, 
                  Emploeeys.code == FctSchedule.code_emploeey)\
            .filter(Emploeeys.id_department == id_department,
                    FctSchedule.status == "wait")\
            .all()

        session.commit()
        print(create_list_of_schedules(data))
        return create_list_of_schedules(data)
    except:
        session.rollback()
        print('Rolled back')
        raise


def update_employee_status(code: str, status="reject"):
    """
    """
    from sqlalchemy import func
    session = db.session
    try:
        max_dt = session.query(func.max(FctSchedule.week_start_date))\
            .filter(FctSchedule.status == "wait", 
                    FctSchedule.code_emploeey == code)\
            .first()
        print(max_dt)
        data = session.query(FctSchedule)\
            .filter(FctSchedule.status == "wait", 
                    FctSchedule.code_emploeey == code,
                    FctSchedule.week_start_date == max_dt[0])\
            .first()
        print(data)
        data.status = status
        session.commit()
    except:
        session.rollback()
        print('Rolled back')
        raise