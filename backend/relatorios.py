import csv
import io
from fastapi import APIRouter, Depends, Response, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from projeto_ATC.backend.database import get_connection

router = APIRouter(prefix="/relatorios", tags=["relatorios"])

SECRET_KEY = "sua_chave_secreta_super_segura"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return {"id": payload.get("sub"), "tipo": payload.get("tipo")}

@router.get("/tickets_csv")
def exportar_tickets_csv(current_user: dict = Depends(get_current_user)):
    if current_user["tipo"] != "atendente":
        raise HTTPException(status_code=403, detail="Apenas atendentes podem exportar relatórios")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, descricao, prioridade, status_, data_criacao, data_fechamento FROM tickets")
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Título", "Descrição", "Prioridade", "Status", "Data Criação", "Data Fechamento"])
    for r in rows:
        writer.writerow([r.id, r.titulo, r.descricao, r.prioridade, r.status_, r.data_criacao, r.data_fechamento])

    return Response(content=output.getvalue(), media_type="text/csv")