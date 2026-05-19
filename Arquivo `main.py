import os
from fastapi import FastAPI
from .routers import auth_router, user_router, chat_router

app = FastAPI()

# Inclua as rotas aqui
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(chat_router.router)
