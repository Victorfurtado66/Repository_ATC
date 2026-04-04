from fastapi import FastAPI
from auth import router as auth_router
from usuarios import router as usuarios_router
from tickets import router as tickets_router
from database import get_connection

app = FastAPI(title="Plataforma de Atendimento ao Cliente")

app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(tickets_router)

# ✅ Testa a conexão ao iniciar o servidor
@app.on_event("startup")
def verificar_conexao():
    try:
        conn = get_connection()
        conn.close()
        print("✅ Conexão com o banco de dados bem-sucedida!")
    except Exception as e:
        print(f"❌ Erro ao conectar com o banco de dados: {e}")
```

Assim quando você rodar `uvicorn main:app --reload` vai aparecer no terminal:
```
✅ Conexão com o banco de dados bem-sucedida!
