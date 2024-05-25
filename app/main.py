import os
import requests
from random import randint
from datetime import datetime

import vk_botting
from vk_botting.keyboard import Keyboard, KeyboardColor
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session

from db_obj.employee import Employees
from db_obj.schedule import Schedule
from db_obj.direct import Direct

load_dotenv("/home/joshua/Документы/myStudy/botMcdSchedule/.env")

API_VK_TOKEN = os.environ.get("VK_API_TOKEN")
HOST = os.environ.get("DB_HOST")
PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB = os.environ.get("DATA_BASE")

DATABASE = {
        'drivername': 'postgresql',
        'host': HOST,
        'port': PORT,
        'username': DB_USER,
        'password': DB_PASSWORD,
        'database': DB,
        'query': {'sslmode': 'prefer'}
    }

bot = vk_botting.Bot('/')

def get_vk_id_direct():

    with Session(autoflush=False, bind=engine) as db:
        _query = db.query(Direct.vk_id)
        # direct_id = _query.all()
        direct_id = _query.first()[0]

    return direct_id
    
def get_keyboard(keyboard):

    keyboard.add_button('[CREATE SCHEDULE]')
    keyboard.add_button('[SEND SCHEDULE]')
    keyboard.add_line()
    keyboard.add_button('[]')
    keyboard.add_line()
    keyboard.add_button('[FAQ]')

    return keyboard

def get_aplly_keyboard(keyboard, code: int):
    # keyboard.add_button(f'{vk_id}', KeyboardColor.POSITIVE)
    # keyboard.add_button(f'-{vk_id}', KeyboardColor.NEGATIVE)
    keyboard.add_button(f'{code}', KeyboardColor.POSITIVE)
    keyboard.add_button(f'-{code}', KeyboardColor.NEGATIVE)
    print(keyboard)
    return keyboard


def get_employees_data(templates: str) -> list:
    """
    """

    exmpl_list = templates.split(sep=' ')

    return [exmpl_list[1], exmpl_list[2], exmpl_list[-1].split(sep=',')]


def exchange_day_off(schedule: list):
    """
    """
    for ind, elm in enumerate(schedule):
        if elm == '0000-0000':
            schedule[ind] = 'Day off'
    
    return schedule


def fill_dim_employees(id: str, vk_id: str, code: int, engine: object):
    """
    """

    with Session(autoflush=False, bind=engine) as db:
        employee = Employees(id=id, code=code, vk_id=vk_id, create_data=datetime.now().date())
        db.add(employee)
        db.commit()
        print("COMPLETE RECORD DATA EMPLOYEE")


def send_schedule_to_direct(id_direct: int, msg_shedule: str, keybord: dict):
    msg = f"{datetime.now()} Расписание на утверждение: {msg_shedule}"
    url = f"https://api.vk.com/method/messages.send?v=5.199&access_token={API_VK_TOKEN}&user_id={id_direct}&random_id={randint(0, 2)}&message={msg}&keyboard={keybord}"
    # url = f"https://api.vk.com/method/messages.send?access_token={API_VK_TOKEN}&user_id={id_direct}&random_id=0&message={42}&keyboard={keybord}"
    print(url)
    payload = {}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.status_code)
    print(response.text)
    if response.status_code == 200:
        print(200)
    else:
        print(0)


def fill_fct_schedule(code: int, schedule: list):
    """
    """
    s_monday, s_tuesday, s_wednesday, s_thursday, s_friday, s_saturday, s_sunday = schedule

    with Session(autoflush=False, bind=engine) as db:
        new_schedule = Schedule(code=code, s_monday=s_monday, s_tuesday=s_tuesday, 
                                s_wednesday=s_wednesday, s_thursday=s_thursday, s_friday=s_friday,
                                s_saturday=s_saturday, s_sunday=s_sunday, create_data=datetime.now().date())
        
        db.add(new_schedule)        
        db.commit()
        print("COMPLETE RECORD DATA SCHEDULE")


@bot.listen()
async def on_ready():
    print(f'Logged in as {bot.group.name}')
    print(get_vk_id_direct(), type(get_vk_id_direct()))


@bot.listen()
async def on_message_new(message):
    global is_schedule, is_prime, is_incorrect_data, schedule, code, vk_id

    if message.text == '[CREATE SCHEDULE]':
        is_schedule = True 
        await message.send("""Для отправки своего расписания на утверждение необходимо отправить сообщение по следующему шаблону
                           
                           !ВАЖНО! Шаблон начинается с прописной латинской 's'
                           
                           's <Табельный Номер> <Код сотрудника> <Время работы>'

                           !ВАЖНО! Между каждым блоком в шаблоне ставится знак ПРОБЕЛА

                           <Табельный Номер> - это шестизначный номер
                           <Код сотрудника> - это трехзначный номер

                           ПРИМЕЧАНИЕ:
                           -- длина <Код сотрудника> всегда должна быть равна трем (3) символам

                            ПРИМЕР КОРРЕКТНОГО ЗАПОЛНЕНИЯ КОДА СОТРУДНИКА:
                           
                           (Правильно) 001
                           (Неправильно) 5
                           (Неправильно) 13
                           (Правильно) 027
                           (Правильно) 120

                           <Время работы> необходимо заполнять по шаблону: ЧасыМинуты-ЧасыМинуты

                           ПРИМЕЧАНИЕ: 
                           -- для указания дня, когда у тебя выходной необходимо заполнить шаблон нулями - 0000-0000
                           -- записи <Время работы> разделяются знаком запятой
                           -- при заполнении нужно помнить, что дни учитываются с понедельника по воскресенье

                            ПРИМЕР ЗАПОЛНЕНИЯ ОТВЕТА:
                           
                           s 468400 102 0700-1600,1600-0000,0000-0000,0000-0000,1600-2300,0700-0000,0700-0000

                           Так по шаблону видно, что:

                           -- s - отправка сообщения по расписанию
                           -- 468400 - табельный номер работника
                           -- 102 - код работника
                           -- <Время работы>:
                           Понедельник: 07:00-16:00
                           Вторник: 16:00-00:00
                           Среда: Выходной
                           Четверг: Выходной
                           Пятница: 16:00-23:00
                           Суббота: 07:00-00:00
                           Воскресенье: 07:00-00:00""")
        
    if message.text.startswith('s') and is_schedule:
        is_schedule = False

        vk_id = message.from_id
        
        if len(message.text) == 82:
            id, code, schedule = get_employees_data(message.text)
        else:
            is_incorrect_data = True
            id, code, schedule = ['000000', '000', ['****-****' for i in range(7)]]
        
        if is_incorrect_data:
            msg = "Неккоретно заполнен шаблон с данными\nДля повторного ввода необходимо кликнуть по кнопке [CREATE SCHEDULE]"
            is_incorrect_data = False
            schedule = []
        else:
            msg = f"""
            -- Вы запросили следующее расписание на новую неделю --

            Понедельник: {schedule[0] if schedule[0] != '0000-0000' else 'Выходной'}
            Вторник: {schedule[1] if schedule[1] != '0000-0000' else 'Выходной'}
            Среда: {schedule[2] if schedule[2] != '0000-0000' else 'Выходной'}
            Четверг: {schedule[3] if schedule[3] != '0000-0000' else 'Выходной'}
            Пятница: {schedule[4] if schedule[4] != '0000-0000' else 'Выходной'}
            Суббота: {schedule[5] if schedule[5] != '0000-0000' else 'Выходной'}
            Воскресенье: {schedule[6] if schedule[6] != '0000-0000' else 'Выходной'}
            """  

        schedule = exchange_day_off(schedule=schedule)
        fill_fct_schedule(code=code, schedule=schedule)    

        try:
            fill_dim_employees(id, vk_id, code, engine)
        except Exception as exp:
            print(exp)
            print("Запись уже существует")

        await message.reply(message=f"Thank you, we received your data and started working\n{msg}")

    if message.text == '[SEND SCHEDULE]' and schedule:
        is_prime = True
        
        msg = f"""
        -- Желаемое расписание сотрудника {code} -- 
        Понедельник: {schedule[0] if schedule[0] != '0000-0000' else 'Выходной'}
        Вторник: {schedule[1] if schedule[1] != '0000-0000' else 'Выходной'}
        Среда: {schedule[2] if schedule[2] != '0000-0000' else 'Выходной'}
        Четверг: {schedule[3] if schedule[3] != '0000-0000' else 'Выходной'}
        Пятница: {schedule[4] if schedule[4] != '0000-0000' else 'Выходной'}
        Суббота: {schedule[5] if schedule[5] != '0000-0000' else 'Выходной'}
        Воскресенье: {schedule[6] if schedule[6] != '0000-0000' else 'Выходной'}"""

        try:
            bot_keyboard.get_empty_keyboard()
        except Exception as exp:
            print(exp)

        send_schedule_to_direct(id_direct=VK_ID_DIRECT, msg_shedule=msg, keybord=get_aplly_keyboard(inline_keybord, code=code))

        await message.reply(message="Расписание отправлено на утверждение")
    elif message.text == '[SEND SCHEDULE]' and not schedule:
        await message.reply(message="Сначало необходимо сформировать расписание")


@bot.listen()
async def on_chat_create(message):
    msg = "Для вызова подсказки по работе бота введите команду /help"
    await message.send(message=msg)


@bot.listen()
async def on_conversation_start(message):
    msg = "Для вызова подсказки по работе бота введите команду /help"
    await message.send(message=msg)


@bot.command(name='keyboard')
async def receive_keyboard(context):
    keyboard = get_keyboard(bot_keyboard)
    await context.send('-', keyboard=keyboard)


@bot.command(name='help')
async def receive_help(context):
    await context.send('For summoned "keybord" writing /keyboard')

templates = """
| Код сотрудника | Понедельник |   Вторник   |    Среда    |   Четверг   |   Пятница   |   Суббота   | Воскресенье |
|----------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------|
"""
foo = "| {code:>14} | {schedule[0]:>11} | {schedule[1]:>11} | {schedule[2]:>11} | {schedule[3]:>11} | {schedule[4]:>11} | {schedule[5]:>11} | {schedule[6]:>11} |"

if __name__ == "__main__":
    engine = create_engine(URL(**DATABASE))

    VK_ID_DIRECT = get_vk_id_direct()
    print(VK_ID_DIRECT)

    bot_keyboard = Keyboard()
    inline_keybord = Keyboard(inline=True)

    is_schedule, is_prime, is_incorrect_data = False, False, False
    number_employee, id_employee = '', ''
    schedule = []
    code, vk_id = 0, 0

    bot.run(token=API_VK_TOKEN) 