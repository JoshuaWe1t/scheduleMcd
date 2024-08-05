from sqlalchemy import  Column, Integer, String, Date, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Schedule(Base):
    __tablename__ = "fct_schedule"

    id = Column(Integer, Sequence('schedule_id_seq'), primary_key=True)
    code = Column(Integer)
    s_monday = Column(String)
    s_tuesday = Column(String)
    s_wednesday = Column(String)
    s_thursday = Column(String)
    s_friday = Column(String)
    s_saturday = Column(String)
    s_sunday = Column(String)
    create_data = Column(Date)

    def __init__(self, code, s_monday,
                s_tuesday, s_wednesday, s_thursday,
                s_friday, s_saturday, s_sunday, create_data):

        self.code = code
        self.s_monday = s_monday
        self.s_tuesday = s_tuesday
        self.s_wednesday = s_wednesday
        self.s_thursday = s_thursday
        self.s_friday = s_friday
        self.s_saturday = s_saturday
        self.s_sunday = s_sunday
        self.create_data = create_data