from fastapi import APIRouter
from fastapi_sqlalchemy import db


from models import message as Message
from src.schemas.message_schema import MessageCreate as SchemaMessage
from src.schemas.message_schema import Message as Messages

routes = APIRouter()


@routes.post("/add_message_pacient/{key}")
async def add_message_pacient(key: int, msg: SchemaMessage):
    if key == 12:
        message = Message.Message(person_id=msg.person_id, message=msg.message)
        db.session.add(message)
        db.session.commit()
        db.session.refresh(message)
        return message
    else:
        return "ERROR"
