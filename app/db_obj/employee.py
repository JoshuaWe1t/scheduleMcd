from sqlalchemy import  Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Employees(Base):
    __tablename__ = "dim_employees"
 
    id = Column(String, primary_key=True)
    code = Column(Integer)
    vk_id = Column(String)
    create_data = Column(Date)

    def __init__(self, id, code, vk_id, create_data):
        self.id = id
        self.code = code
        self.vk_id = vk_id
        self.create_data = create_data