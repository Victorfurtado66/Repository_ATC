from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from projeto_ATC.backend.database import get_connection

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

SECRET_KEY = "sua_chave_secreta_super_segura"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"id": payload.get("sub"), "tipo": payload.get("tipo")}
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.get("/")
def dashboard_metrics(current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    # Tickets abertos
    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status_ = 'aberto'")
    abertos = cursor.fetchone()[0]

    # Tickets fechados
    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status_ = 'fechado'")
    fechados = cursor.fetchone()[0]

    # Tempo médio de fechamento (em horas)
    cursor.execute("""
        SELECT AVG(DATEDIFF(HOUR, data_criacao, data_fechamento))
        FROM tickets
        WHERE status_ = 'fechado' AND data_fechamento IS NOT NULL
    """)
    tempo_medio = cursor.fetchone()[0]

    # Tickets por prioridade
    cursor.execute("""
        SELECT prioridade, COUNT(*) 
        FROM tickets 
        GROUP BY prioridade
    """)
    prioridades = {row[0]: row[1] for row in cursor.fetchall()}

    conn.close()

    return {
        "tickets_abertos": abertos,
        "tickets_fechados": fechados,
        "tempo_medio_resposta_horas": tempo_medio,
        "tickets_por_prioridade": prioridades
    }