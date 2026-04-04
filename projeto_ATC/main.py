from fastapi import FastAPI
from usuarios import router as usuarios_router
from tickets import router as tickets_router
from auth import router as auth_router

app = FastAPI(title="Plataforma de Atendimento ao Cliente")

app.include_router(usuarios_router)
app.include_router(tickets_router)
app.include_router(auth_router)


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
