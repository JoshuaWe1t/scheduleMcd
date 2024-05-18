from sqlalchemy import  Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Direct(Base):
    __tablename__ = "dim_direct"
 
    vk_id = Column(Integer, primary_key=True)

    def __init__(self, vk_id):
        self.vk_id = vk_id
