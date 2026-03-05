from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from projeto_ATC.backend.database import get_connection
from datetime import datetime

router = APIRouter(prefix="/tickets", tags=["tickets"])

SECRET_KEY = "sua_chave_secreta_super_segura"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return {"id": payload.get("sub"), "tipo": payload.get("tipo")}

# Criar ticket (cliente)
from pydantic import BaseModel

class TicketCreate(BaseModel):
    titulo: str
    descricao: str
    prioridade: str = "media"

@router.post("/")
def criar_ticket(ticket: TicketCreate, current_user: dict = Depends(get_current_user)):
    if current_user["tipo"] != "cliente":
        raise HTTPException(status_code=403, detail="Apenas clientes podem abrir tickets")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tickets (cliente_id, titulo, descricao, prioridade, status_, data_criacao) VALUES (?, ?, ?, ?, ?, ?)",
        (current_user["id"], ticket.titulo, ticket.descricao, ticket.prioridade, "aberto", datetime.now())
    )
    conn.commit()
    conn.close()
    return {"msg": "Ticket criado com sucesso"}
# Listar tickets
@router.get("/")
def listar_tickets(current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    if current_user["tipo"] == "cliente":
        cursor.execute("SELECT id, titulo, status_, prioridade FROM tickets WHERE cliente_id = ?", current_user["id"])
    else:  # atendente vê todos
        cursor.execute("SELECT id, titulo, status_, prioridade FROM tickets")

    rows = cursor.fetchall()
    conn.close()
    return [{"id": r.id, "titulo": r.titulo, "status": r.status_, "prioridade": r.prioridade} for r in rows]

# Atualizar ticket (atendente)
@router.put("/{ticket_id}")
def atualizar_ticket(ticket_id: int, status_: str = None, prioridade: str = None, current_user: dict = Depends(get_current_user)):
    if current_user["tipo"] != "atendente":
        raise HTTPException(status_code=403, detail="Apenas atendentes podem atualizar tickets")

    conn = get_connection()
    cursor = conn.cursor()

    # Se status for "fechado", grava data_fechamento
    if status_ == "fechado":
        cursor.execute(
            "UPDATE tickets SET status_ = ?, prioridade = ISNULL(?, prioridade), atendente_id = ?, data_fechamento = ? WHERE id = ?",
            status_, prioridade, current_user["id"], datetime.now(), ticket_id
        )
    else:
        cursor.execute(
            "UPDATE tickets SET status_ = ISNULL(?, status_), prioridade = ISNULL(?, prioridade), atendente_id = ? WHERE id = ?",
            status_, prioridade, current_user["id"], ticket_id
        )

    conn.commit()
    conn.close()
    return {"msg": "Ticket atualizado com sucesso"}