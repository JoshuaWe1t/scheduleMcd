import sqlalchemy as sa
import sqlalchemy.orm as sao
from flask_login import UserMixin

from scheduleMcd.backend.app import db, login
from scheduleMcd.backend.config import SCHEMA

Base = db.Model

class FctSchedule(Base):
    __tablename__ = 'fct_schedule'
    __table_args__ = {'schema': SCHEMA}
    id = sa.Column(sa.Integer, primary_key=True)
    code_emploeey = sa.Column(sa.String(200), sa.ForeignKey(f'{SCHEMA}.dim_emploeeys.code'), nullable=False)
    mon = sa.Column(sa.String(50), nullable=False)
    tue = sa.Column(sa.String(50), nullable=False)
    wed = sa.Column(sa.String(50), nullable=False)
    thu = sa.Column(sa.String(50), nullable=False)
    fri = sa.Column(sa.String(50), nullable=False)
    sat = sa.Column(sa.String(50), nullable=False)
    sun = sa.Column(sa.String(50), nullable=False)
    record_dt = sa.Column(sa.Date, nullable=False)
    week_num = sa.Column(sa.Integer, nullable=False)
    week_start_date = sa.Column(sa.Date, nullable=False)
    status = sa.Column(sa.String(50), nullable=False)

    # Связь с моделью Emploeeys
    employee = sao.relationship("Emploeeys", back_populates="schedules")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Emploeeys(UserMixin, Base):
    __tablename__ = 'dim_emploeeys'
    __table_args__ = {'schema': SCHEMA}
    id = sa.Column(sa.Integer, nullable=False) # Уникальный публичный номер сотрудника
    code = sa.Column(sa.String(200), nullable=False, primary_key=True) # Уникальный приватный номер сотрудника
    first_name = sa.Column(sa.String(200), nullable=False)
    last_name = sa.Column(sa.String(200), nullable=False)
    middle_name = sa.Column(sa.String(200), nullable=True)
    id_specialization = sa.Column(sa.Integer, sa.ForeignKey(f'{SCHEMA}.dim_specialization.id'))#sa.Column(sa.Integer, nullable=False)
    pswrd = sa.Column(sa.String(200), nullable=False)
    id_department = sa.Column(sa.Integer, sa.ForeignKey(f'{SCHEMA}.dim_department.id'))#sa.Column(sa.Integer, nullable=False) # Департамент сотрудника
    role = sa.Column(sa.String(20), nullable=False)

    # Обратная связь с расписаниями и специализацией
    schedules = sao.relationship("FctSchedule", back_populates="employee", cascade="all, delete-orphan")
    specialization = sao.relationship("Specialization", back_populates="employees", cascade="all")
    department = sao.relationship("Department", back_populates="employees", cascade="all")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def get_id(self):
        return self.code  

    # Метод для проверки пароля
    def check_password(self, password):
        if password == self.pswrd:
            return True
        return False
    

# @login.user_loader
# def load_user(code):
#     return db.session.get(Emploeeys, code)
@login.user_loader
def load_user(code):
    print(f"Trying to load user by code: {code}, type: {type(code)}")
    user = db.session.get(Emploeeys, code)
    if user:
        print(f"Found user: {user}")
    else:
        print("User not found")
    return user

class Specialization(Base):
    __tablename__ = 'dim_specialization'
    __table_args__ = {'schema': SCHEMA}
    id = sa.Column(sa.Integer, primary_key=True)  # Первичный ключ для специализаций
    name = sa.Column(sa.String(200), nullable=False)  # Название специализации
    description = sa.Column(sa.String(200), nullable=False)  # Описание

    # Связь с сотрудниками
    employees = sao.relationship("Emploeeys", back_populates="specialization")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Department(Base):
    __tablename__ = 'dim_department'
    __table_args__ = {'schema': SCHEMA}
    id = sa.Column(sa.Integer, primary_key=True)  # Первичный ключ департамента
    name = sa.Column(sa.String(200), nullable=False)  # Наименование департамента

    # Связь с сотрудниками
    employees = sao.relationship("Emploeeys", back_populates="department")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
