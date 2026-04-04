from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from database import get_connection
from models import TicketCreate
from config import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/tickets", tags=["tickets"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

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
def criar_ticket(ticket: TicketCreate, user_id: str = Depends(get_current_user)):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # ✅ Parâmetros em tupla e GETDATE() correto para SQL Server
        cursor.execute(
            """
            INSERT INTO Tickets (cliente_id, atendente_id, titulo, descricao, status, prioridade, data_criacao)
            VALUES (?, ?, ?, ?, ?, ?, GETDATE())
            """,
            (ticket.cliente_id, ticket.atendente_id, ticket.titulo, ticket.descricao, ticket.status, ticket.prioridade)
        )
        conn.commit()
        return {"message": "Ticket criado com sucesso", "titulo": ticket.titulo, "usuario": user_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# ✅ Rota para listar tickets
@router.get("/")
def listar_tickets(user_id: str = Depends(get_current_user)):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Tickets")
        tickets = cursor.fetchall()
        colunas = [col[0] for col in cursor.description]
        return [dict(zip(colunas, row)) for row in tickets]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# ✅ Rota para deletar ticket
@router.delete("/{ticket_id}")
def deletar_ticket(ticket_id: int, user_id: str = Depends(get_current_user)):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Tickets WHERE id = ?", (ticket_id,))
        conn.commit()
        return {"message": "Ticket removido com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
