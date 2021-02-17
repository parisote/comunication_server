from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi_sqlalchemy import DBSessionMiddleware
from dotenv import load_dotenv
import os
import sys
from src.routes.auth import auth
from src.routes.pacient import pacient
from src.task import message_task
from concurrent.futures import ThreadPoolExecutor
import schedule

app = FastAPI()
executor = ThreadPoolExecutor(4)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
app.add_middleware(DBSessionMiddleware, db_url=os.environ["SQLALCHEMY_DATABASE_URI"])


@app.get("/", response_class=HTMLResponse)
def loginwithCreds(request: Request):
    with open(os.path.join(BASE_DIR, "src/templates/login.html")) as f:
        return HTMLResponse(content=f.read())


def createSchedule():
    executor.submit(message_task.createProcessSendMenssage, account_sid, auth_token)


@app.on_event("startup")
async def startup():
    print("Connecting...")
    createSchedule()


app.include_router(auth.routes)
app.include_router(pacient.routes)


@app.on_event("shutdown")
def shutdown_event():
    schedule.clear()
    executor.shutdown(wait=False)
    print("Shutdown app")
