from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from projeto_ATC.backend.database import get_connection

router = APIRouter(prefix="/historico", tags=["historico"])

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
def listar_historico(current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    if current_user["tipo"] == "cliente":
        cursor.execute(
            "SELECT id, titulo, descricao, prioridade, data_criacao, data_fechamento \
             FROM tickets WHERE cliente_id = ? AND status_ = 'fechado'",
            current_user["id"]
        )
    else:  # atendente vê todos os tickets fechados
        cursor.execute(
            "SELECT id, titulo, descricao, prioridade, data_criacao, data_fechamento \
             FROM tickets WHERE status_ = 'fechado'"
        )

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r.id,
            "titulo": r.titulo,
            "descricao": r.descricao,
            "prioridade": r.prioridade,
            "data_criacao": r.data_criacao,
            "data_fechamento": r.data_fechamento
        }
        for r in rows
    ]