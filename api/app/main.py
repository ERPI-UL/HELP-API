from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from mail import simple_send
from routers import admin, users
from routers import scenarios
from routers import stats
from routers import auth
from routers import easy

import utils

tags_metadata = [
    {
        "name": "auth",
        "description": "Opérations d'authentification",
    }, {
        "name": "users",
        "description": "Opération sur les utilisateurs : création, modification, suppression, listes paginées",
    }, {
        "name": "scenarios",
        "description": "Opération sur les scénarios , machines et leurs composants : création, modification, suppression, listes paginées",
    }, {
        "name": "stats",
        "description": "Opération sur les statistiques : création et supression d'une session d'un scénario, listes paginées ",
    }, {
        "name": "easy",
        "description": "générer un code d'accès rapide , HTTP Long-Polling pour envoyer le token d'authentification à l'appareil XR",
    }, {
        "name": "admin",
        "description": "Opérations réservées aux admins : changer le niveau d'admin d'un utilisateur, supprimer un utilisateur",
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
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(scenarios.router, prefix="/scenarios", tags=["scenarios"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(easy.router, prefix="/easy", tags=["easy"])


# redirect root to docs
@app.get("/")
async def root():
    response = RedirectResponse(url='/docs')
    return response


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

# Mail().send(["fanta.r55000@gmail.com"], "Indico API", "<b>This is HTML message.</b>")
simple_send("fanta.r55000@gmail.com")