from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from projeto_ATC.backend.database import get_connection
from projeto_ATC.backend.models import UsuarioCreate

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/")
def criar_usuario(usuario: UsuarioCreate):
    # Valida tipo
    if usuario.tipo not in ["cliente", "atendente"]:
        raise HTTPException(status_code=400, detail="Tipo inválido. Use 'cliente' ou 'atendente'.")

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Verifica se email já existe
        cursor.execute("SELECT id FROM Usuarios WHERE email = ?", (usuario.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email já cadastrado")

        # Criptografa a senha
        senha_hash = pwd_context.hash(usuario.senha)

        # Insere no banco
        cursor.execute(
            "INSERT INTO Usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
            (usuario.nome, usuario.email, senha_hash, usuario.tipo)
        )
        conn.commit()

        return {"message": "Usuário criado com sucesso", "email": usuario.email}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar usuário: {str(e)}")
    finally:
        conn.close()