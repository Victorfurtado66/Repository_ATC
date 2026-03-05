from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from projeto_ATC.backend.database import get_connection
from datetime import datetime

router = APIRouter(prefix="/mensagens", tags=["mensagens"])

SECRET_KEY = "sua_chave_secreta_super_segura"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"id": payload.get("sub"), "tipo": payload.get("tipo")}
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

# Enviar mensagem
@router.post("/{ticket_id}")
def enviar_mensagem(ticket_id: int, conteudo: str, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    # Verifica se ticket existe
    cursor.execute("SELECT id FROM tickets WHERE id = ?", ticket_id)
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Ticket não encontrado")

    cursor.execute(
        "INSERT INTO mensagens (ticket_id, remetente_id, conteudo, data_envio) VALUES (?, ?, ?, ?)",
        ticket_id, current_user["id"], conteudo, datetime.now()
    )
    conn.commit()
    conn.close()
    return {"msg": "Mensagem enviada com sucesso"}

# Listar mensagens de um ticket
@router.get("/{ticket_id}")
def listar_mensagens(ticket_id: int, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT m.id, m.conteudo, m.data_envio, u.nome, u.tipo \
         FROM mensagens m JOIN usuarios u ON m.remetente_id = u.id \
         WHERE m.ticket_id = ? ORDER BY m.data_envio ASC",
        ticket_id
    )
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r.id,
            "conteudo": r.conteudo,
            "data_envio": r.data_envio,
            "remetente": r.nome,
            "tipo": r.tipo
        }
        for r in rows
    ]