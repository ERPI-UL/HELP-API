from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from routers import admin, users
from routers import scenarios
from routers import stats
from routers import auth
from routers import easy

import utils

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
