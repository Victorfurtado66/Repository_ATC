from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    tipo: str  # cliente ou atendente

class TicketCreate(BaseModel):
    cliente_id: int
    atendente_id: int | None = None
    titulo: str
    descricao: str
    status: str
    prioridade: str