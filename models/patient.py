from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Pacient(Base):
    __tablename__ = "pacient"
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer)
    last_name = Column(String(255))
    first_name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(255))
