from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from projeto_ATC.backend import usuarios, tickets, auth

app = FastAPI(title="Projeto ATC")

# Configuração de CORS para permitir comunicação com o frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["http://localhost:3000"] para restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(usuarios.router)
app.include_router(tickets.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "API Projeto ATC rodando com sucesso 🚀"}