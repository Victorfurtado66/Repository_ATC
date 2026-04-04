from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from database import get_connection
from models import UsuarioCreate
from config import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/usuarios", tags=["usuarios"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        tipo: str = payload.get("tipo")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"id": user_id, "tipo": tipo}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.post("/")
def criar_usuario(usuario: UsuarioCreate, current_user: dict = Depends(get_current_user)):
    if current_user["tipo"] != "atendente":
        raise HTTPException(status_code=403, detail="Apenas atendentes podem criar usuários")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        # ✅ Parâmetro em tupla
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", (usuario.email,))
        existente = cursor.fetchone()
        if existente:
            raise HTTPException(status_code=400, detail="Email já cadastrado")

        senha_hash = pwd_context.hash(usuario.senha)
        # ✅ Parâmetros em tupla
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
            (usuario.nome, usuario.email, senha_hash, usuario.tipo)
        )
        conn.commit()
        return {"message": "Usuário criado com sucesso", "email": usuario.email}
    except HTTPException:
        # ✅ Deixa o HTTPException passar normalmente
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
