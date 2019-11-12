from sqlalchemy import Column, Integer, String
from . import Base


class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    name = Column(String)
