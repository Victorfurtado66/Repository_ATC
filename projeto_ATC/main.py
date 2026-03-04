from fastapi import FastAPI
from usuarios import router as usuarios_router
from tickets import router as tickets_router
from auth import router as auth_router

app = FastAPI(title="Plataforma de Atendimento ao Cliente")

app.include_router(usuarios_router)
app.include_router(tickets_router)
app.include_router(auth_router)