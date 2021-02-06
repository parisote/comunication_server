from fastapi import Depends, status, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.templating import Jinja2Templates
import os


routes = APIRouter()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET = "secret-key"
pth = os.path.dirname(BASE_DIR)
templates = Jinja2Templates(directory=os.path.join(pth, "templates"))


manager = LoginManager(SECRET, tokenUrl="/auth/login", use_cookie=True)
manager.cookie_name = "some-name"

DB = {"username": {"password": "qwertyuiop"}}


@manager.user_loader
def load_user(username: str):
    user = DB.get(username)
    return user


@routes.post("/auth/login")
def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    user = load_user(username)
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException
    access_token = manager.create_access_token(
        data={"sub": username}
    )
    resp = RedirectResponse(url="/private", status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp, access_token)
    return resp


@routes.get("/private")
def getPrivateendpoint(_=Depends(manager)):
    return "You are an authentciated user"
