from sqlalchemy import  Column, Integer, String, Date, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ScheduleUpdate(Base):
    __tablename__ = "fct_schedule_update"

    id = Column(Integer, Sequence('schedule_id_seq'), primary_key=True)
    code = Column(Integer)
    s_monday = Column(String)
    s_tuesday = Column(String)
    s_wednesday = Column(String)
    s_thursday = Column(String)
    s_friday = Column(String)
    s_saturday = Column(String)
    s_sunday = Column(String)
    is_uprove = Column(Integer)
    is_reject = Column(Integer)
    decided_date = Column(Date, nullable=True)
    create_data = Column(Date)
    
    def __init__(self, code, s_monday,
                s_tuesday, s_wednesday, s_thursday,
                s_friday, s_saturday, s_sunday, 
                is_uprove, is_reject, decided_date, 
                create_data):

        self.code = code
        self.s_monday = s_monday
        self.s_tuesday = s_tuesday
        self.s_wednesday = s_wednesday
        self.s_thursday = s_thursday
        self.s_friday = s_friday
        self.s_saturday = s_saturday
        self.s_sunday = s_sunday
        self.is_uprove = is_uprove
        self.is_reject = is_reject
        self.decided_date = decided_date
        self.create_data = create_data