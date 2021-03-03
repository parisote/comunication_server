from pydantic import BaseModel
from enum import Enum


class sendEnum(str, Enum):
    SENT = 'SENT'
    NOT_SENT = 'NOT_SENT'


class MessageBase(BaseModel):
    person_id: int


class MessageCreate(MessageBase):
    person_id: int
    message: str
    phone_number: int


class Message(MessageBase):
    person_id: int
    message: str
    phone_number: int

    class Config:
        orm_mode = True
