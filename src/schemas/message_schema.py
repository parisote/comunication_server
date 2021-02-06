from pydantic import BaseModel


class MessageBase(BaseModel):
    person_id: int


class MessageCreate(MessageBase):
    person_id: int
    message: str


class Message(MessageBase):
    person_id: int
    message: str

    class Config:
        orm_mode = True
