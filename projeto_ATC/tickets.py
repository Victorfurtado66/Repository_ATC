from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from database import get_connection
from models import TicketCreate

router = APIRouter(prefix="/tickets", tags=["tickets"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = "sua_chave_secreta_super_segura"
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.post("/")
def criar_ticket(ticket: TicketCreate, user_id: int = Depends(get_current_user)):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO Tickets (cliente_id, atendente_id, titulo, descricao, status, prioridade, data_criacao)
            VALUES (?, ?, ?, ?, ?, ?, GETDATE())
            """,
            ticket.cliente_id,
            ticket.atendente_id,
            ticket.titulo,
            ticket.descricao,
            ticket.status,
            ticket.prioridade
        )
        conn.commit()

        return {"message": "Ticket criado com sucesso", "titulo": ticket.titulo, "usuario": user_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()