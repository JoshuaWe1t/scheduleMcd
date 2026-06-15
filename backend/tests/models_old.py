import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

from scheduleMcd.backend.tests.engine import ENGINE, SCHEMA

Session = sessionmaker()
session = Session(bind=ENGINE)

Base = declarative_base()

class FctSchedule(Base):
    __tablename__ = 'fct_schedule'
    __table_args__ = {'schema': SCHEMA}
    id = db.Column(db.Integer, primary_key=True)
    code_emploeey = db.Column(db.String(200), db.ForeignKey(f'{SCHEMA}.dim_emploeeys.code'), nullable=False)
    mon = db.Column(db.String(50), nullable=False)
    tue = db.Column(db.String(50), nullable=False)
    wed = db.Column(db.String(50), nullable=False)
    thu = db.Column(db.String(50), nullable=False)
    fri = db.Column(db.String(50), nullable=False)
    sat = db.Column(db.String(50), nullable=False)
    sun = db.Column(db.String(50), nullable=False)
    record_dt = db.Column(db.Date, nullable=False)
    week_num = db.Column(db.Integer, nullable=False)
    week_start_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    # Связь с моделью Emploeeys
    employee = relationship("Emploeeys", back_populates="schedules")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Emploeeys(Base):
    __tablename__ = 'dim_emploeeys'
    __table_args__ = {'schema': SCHEMA}
    id = db.Column(db.Integer, nullable=False) # Уникальный публичный номер сотрудника
    code = db.Column(db.String(200), nullable=False, primary_key=True) # Уникальный приватный номер сотрудника
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    middle_name = db.Column(db.String(200), nullable=True)
    id_specialization = db.Column(db.Integer, db.ForeignKey(f'{SCHEMA}.dim_specialization.id'))#db.Column(db.Integer, nullable=False)
    pswrd = db.Column(db.String(200), nullable=False)
    id_department = db.Column(db.Integer, db.ForeignKey(f'{SCHEMA}.dim_department.id'))#db.Column(db.Integer, nullable=False) # Департамент сотрудника

    # Обратная связь с расписаниями и специализацией
    schedules = relationship("FctSchedule", back_populates="employee", cascade="all, delete-orphan")
    specialization = relationship("Specialization", back_populates="employees", cascade="all")
    department = relationship("Department", back_populates="employees", cascade="all")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Specialization(Base):
    __tablename__ = 'dim_specialization'
    __table_args__ = {'schema': SCHEMA}
    id = db.Column(db.Integer, primary_key=True)  # Первичный ключ для специализаций
    name = db.Column(db.String(200), nullable=False)  # Название специализации
    description = db.Column(db.String(200), nullable=False)  # Описание

    # Связь с сотрудниками
    employees = relationship("Emploeeys", back_populates="specialization")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Department(Base):
    __tablename__ = 'dim_department'
    __table_args__ = {'schema': SCHEMA}
    id = db.Column(db.Integer, primary_key=True)  # Первичный ключ департамента
    name = db.Column(db.String(200), nullable=False)  # Наименование департамента

    # Связь с сотрудниками
    employees = relationship("Emploeeys", back_populates="department")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

Base.metadata.create_all(bind=ENGINE)