from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from projeto_ATC.backend.database import get_connection

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "sua_chave_secreta_super_segura"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, senha, tipo FROM usuarios WHERE email = ?", form_data.username)
    user = cursor.fetchone()
    conn.close()

    if not user or not pwd_context.verify(form_data.password, user.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token_data = {"sub": str(user.id), "tipo": user.tipo}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}