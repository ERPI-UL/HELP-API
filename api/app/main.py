import jwt

from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from routers import users
from routers import scenarios
from routers import sessions
from routers import auth

import Models
import random
import utils

import socketio

tags_metadata = [
    {
        "name": "auth",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    }, {
        "name": "users",
        "description": "Manage users. So _fancy_ they have their own docs."
    }, {
        "name": "scenarios",
        "description": "Manage scenarios. So _fancy_ they have their own docs."
    }, {
        "name": "stats",
        "description": "Manage stats. So _fancy_ they have their own docs."
    }
]

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]


app = FastAPI(
    title="Indico API",
    description="API pour le site web et les applications XR indico",
    contact={
        "name": "Antonin Rousseau",
        "url": "https://antoninrousseau.fr",
        "email": "antonin.rousseau55000@gmail.com",
    },
    tags_metadata=tags_metadata
)

sio = socketio.AsyncServer(
    async_mode="asgi", cors_allowed_origins='*', cors_credentials=True)
socket_app = socketio.ASGIApp(sio)

app.mount("/socketio/", socket_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(scenarios.router, prefix="/scenarios", tags=["scenarios"])
app.include_router(sessions.router, prefix="/stats", tags=["stats"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
easyAuth = {
    '1234': {"sid": "rehetjhnepjohn", "token": 'tokenbidon'},
}


def getEasyCode():
    run = True
    while(run):
        x = ''.join(random.choices('123456789', k=5))
        run = x in easyAuth
    easyAuth[x] = 'tokenbidon'
    return x


# redirect root to docs


@app.get("/")
async def root():
    response = RedirectResponse(url='/docs')
    return response


@sio.on('join')
async def join(sid, *args, **kwargs):
    await app.sio.emit('lobby', 'User joined')


@sio.on('easy/getCode')
async def getEasy(sid, *args, **kwargs):
    code = getEasyCode()
    easyAuth[code] = sid
    await app.sio.emit('easy/setCode', code)


@sio.on("connect")
async def connect(sid, env):
    print("on connect")


@sio.on('easy/login')
async def login(sid, *args, **kwargs):
    code = kwargs['code']
    if code in easyAuth:
        await app.sio.emit('easy/loginSuccess', easyAuth[code])
    else:
        await app.sio.emit('easy/loginFailed', 'Code not found')
# @app.get("/easy")
# async def get_easy():
#     return {'code': getEasyCode()}


# @app.get("/easy/{code}")
# async def get_easy_code(code: str):
#     return {'token': easyAuth[code]}


@app.post("/easy")
async def easy_login(code: Models.Easy, form: OAuth2PasswordRequestForm = Depends()):
    user = await utils.authenticate_user(form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utiliateur ou mot de passe incorrect",
        )
    if code.code not in easyAuth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Code appareil invalide",
        )
    easyAuth[code.code] = code.token
    # await app.sio.emit('easy/setToken', code.token,to=easyAuth[code.code].sid)
    easyAuth.pop(code.code)
    print(code.token)
    return {'ok'}

@app.get('/testdoitetreco')
async def test(token: str = Depends(utils.oauth2_scheme)):
    return {'ok': 'ok'}


@app.get('/ping')
async def ping():
    return {'ping': 'pong'}
@app.get('/init')
async def init():
    await utils.initAdmin()
    return {'init': 'ok'}
register_tortoise(
    app,
    db_url=utils.DB_URL,
    modules={'models': ['Models']},
    generate_schemas=True,
    add_exception_handlers=True
)
Models.UserinToken(id=9, username='furwaz', adminLevel=1)