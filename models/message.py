from sqlalchemy.ext.declarative import declarative_base
import enum
from sqlalchemy import Column, Integer, String, Enum

Base = declarative_base()


class sendEnum(enum.Enum):
    SENT = 'SENT'
    NOT_SENT = 'NOT_SENT'


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer)
    phone_number = Column(Integer)
    message = Column(String(255))
    send = Column(Enum(sendEnum))
