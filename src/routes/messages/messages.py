from fastapi import APIRouter
from fastapi_sqlalchemy import db

from models import message as Message
from src.schemas.message_schema import MessageCreate as SchemaMessage
from src.schemas.message_schema import Message as Messages

from twilio.rest import Client
from fastapi_utils.tasks import repeat_every
from dotenv import load_dotenv
import os

import mysql.connector


routes = APIRouter()
load_dotenv()
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
HOST = os.getenv('MYSQL_HOST')
USER = os.getenv('MYSQL_USER')
PASSWORD = os.getenv('MYSQL_PASSWORD')
BASE = os.getenv('MYSQL_BASE')
KEY = os.getenv('KEY')
PHONE_SMS = os.getenv('PHONE_SMS')

mydb = mysql.connector.connect(
  host=HOST,
  user=USER,
  password=PASSWORD,
  database=BASE
)

mycursor = mydb.cursor()


@routes.post("/add_message_pacient/{key}", response_model=Messages)
async def add_message_pacient(key: str, msg: SchemaMessage):
    if key == KEY:
        message = Message.Message(person_id=msg.person_id, phone_number=msg.phone_number, message=msg.message, send=Message.sendEnum.NOT_SENT)
        db.session.add(message)
        db.session.commit()
        db.session.refresh(message)
        return message
    else:
        return "ERROR"


@repeat_every(seconds=60*10)
async def searchMessage():
    client = Client(account_sid, auth_token)
    mycursor.execute("SELECT * FROM message WHERE send = 'NOT_SENT'")
    myresult = mycursor.fetchall()
    for x in myresult:
        phone = '+54'+str(x[4])
        client.api.account.messages.create(to=phone, from_=PHONE_SMS, body=x[2])
        sql = "UPDATE message SET send = 'SENT' WHERE id = " + str(x[0])
        mycursor.execute(sql)

    mydb.commit()
    print('MENSAJES ENVIADOS', len(myresult))
