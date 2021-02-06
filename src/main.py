from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi_sqlalchemy import DBSessionMiddleware
from dotenv import load_dotenv
import os
import sys
from src.routes.auth import auth
from src.routes.pacient import pacient


app = FastAPI()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)

app.add_middleware(DBSessionMiddleware, db_url=os.environ["SQLALCHEMY_DATABASE_URI"])


@app.get("/", response_class=HTMLResponse)
def loginwithCreds(request: Request):
    with open(os.path.join(BASE_DIR, "src/templates/login.html")) as f:
        return HTMLResponse(content=f.read())


@app.on_event("startup")
async def startup():
    print("Connecting...")


app.include_router(auth.routes)
app.include_router(pacient.routes)
