import os

import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from fastapi_pagination import add_pagination

import app.utils as utils
from app.routers import (actions, activities, admin, auth, data, easy, language,
                         scenarios, stats, tts, users)

tags_metadata = [
    {
        "name": "auth",
        "description": "Opérations d'authentification",
    }, {
        "name": "users",
        "description": "Opération sur les utilisateurs : création, modification, suppression, listes paginées",
    }, {
        "name": "activities",
        "description": "Opération sur les activités : création, modification, suppression, listes paginées",
    }, {
        "name": "actions",
        "description": "Opération sur les actions : création, modification, suppression",
    }, {
        "name": "stats",
        "description": "Opération sur les statistiques : création et supression d'une session d'un scénario, listes paginées ",
    },  {
        "name": "language",
        "description": "Génération de traduction textuel ou de voix à partir de texte",
    }, {
        "name": "tts",
        "description": "Génération de voix à partir de texte",
    }, {
        "name": "easy",
        "description": "générer un code d'accès rapide , HTTP Long-Polling pour envoyer le token d'authentification à l'appareil XR",
    }, {
        "name": "admin",
        "description": "Opérations réservées aux admins : changer le niveau d'admin d'un utilisateur, supprimer un utilisateur",
    }, {
        "name": "data",
        "description": "Routes permettant d'accéder au contenu qui ne peut pas être public",
    }, {
        "name": "scenarios",
        "description": "Opération sur les scénarios , machines et leurs composants : création, modification, suppression, listes paginées",
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
        "name": "Lorraine Fab Living Lab",
        "url": "https://lf2l.fr"
    },
    version="0.3.0",
    openapi_tags=tags_metadata
)
add_pagination(app)

sio_server = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=origins)
sio_app = socketio.ASGIApp(socketio_server=sio_server, socketio_path='sockets')

app.mount('/ws', app=sio_app)


@sio_server.event
async def connect(sid, environ):
    """Connect a client to the socketio server"""
    print(f'{sid}: connected')
    await sio_server.emit('join', {'sid': sid})


@sio_server.event
async def disconnect(sid):
    """ Disconnect a client from the socketio server"""
    print(f'{sid}: disconnected')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(scenarios.router, prefix="/scenarios", tags=["scenarios"], deprecated=True)
app.include_router(stats.router, prefix="/stats", tags=["stats"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(easy.router, prefix="/easy", tags=["easy"])
app.include_router(tts.router, prefix="/tts", tags=["tts"])
app.include_router(language.router, prefix="/langs", tags=["language"])
app.include_router(data.router, prefix="/data", tags=["data"])
app.include_router(actions.router, prefix="/actions", tags=["actions"])
app.include_router(activities.router, prefix="/activities", tags=["activities"])

models = []
for file in os.listdir('app/models'):
    # si le fichier est un fichier python
    if file.endswith('.py') and file != '__init__.py':
        # on ajoute le nom du fichier sans l'extension
        models.append("app.models." + file[:-3])


@app.on_event("startup")
async def startup_event():
    """ Startup event """
    await Tortoise.init(db_url=utils.DB_URL, modules={'models': models})
    await Tortoise.generate_schemas()
    await utils.init_admin()
    await utils.init_db_with_data()


@app.get("/")
async def root():
    """ Root of the API, redirect to docs"""
    response = RedirectResponse(url='/docs')
    return response


@app.get('/ping')
async def ping():
    """Ping the server to check if it's alive"""
    return {'ping': 'pong'}


register_tortoise(
    app,
    db_url=utils.DB_URL,
    modules={'models': models},
    generate_schemas=True,
    add_exception_handlers=True
)
