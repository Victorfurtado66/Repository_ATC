from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from database import get_connection
from pydantic import BaseModel
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login", response_model=Token)
def login(request: LoginRequest):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # ✅ Parâmetro em tupla
        cursor.execute("SELECT id, senha, tipo FROM usuarios WHERE email = ?", (request.email,))
        usuario = cursor.fetchone()
        if not usuario:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        usuario_id, senha_hash, tipo = usuario
        if not pwd_context.verify(request.senha, senha_hash):
            raise HTTPException(status_code=401, detail="Senha incorreta")
        access_token = create_access_token(
            data={"sub": str(usuario_id), "tipo": tipo},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        # ✅ Deixa o HTTPException passar normalmente
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
