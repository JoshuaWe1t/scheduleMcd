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
from sqlalchemy import update, func, select

from models.employee import Employees
from models.schedule import Schedule
from models.direct import Direct
from models.schedule_update import ScheduleUpdate

load_dotenv("/home/joshua/Документы/myStudy/botMcdSchedule/.env")

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

engine = create_engine(URL(**DATABASE))

stmg = select(Schedule.create_data).where(Schedule.code == 102)


with Session(autoflush=False, bind=engine) as db:
    # получение всех объектов
    people = db.query(Schedule).filter(Schedule.code == 102).\
        filter(Schedule.create_data == db.query(func.max(Schedule.create_data)).\
               filter(Schedule.code == 102)).all()
    
    ch = db.query(func.max(Schedule.create_data)).filter(Schedule.code == 102)
    print(*ch.first())
    # print(type(people))
    # for s in people:
    #     # break
    #     print(f'{s.code}. {s.create_data}')