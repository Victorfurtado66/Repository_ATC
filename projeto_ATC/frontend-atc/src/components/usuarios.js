import React, { useState } from "react";
import api from "../api";
import "./usuario.css";

function Usuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [tipo, setTipo] = useState("cliente");
  const [erro, setErro] = useState("");
  const [sucesso, setSucesso] = useState("");

  const adicionarUsuario = async () => {
    // ✅ Validação básica antes de enviar
    if (!nome || !email || !senha) {
      setErro("Preencha todos os campos!");
      return;
    }
    try {
      // ✅ Token removido daqui, já é adicionado pelo interceptador do api.js
      const response = await api.post("/usuarios", {
        nome,
        email,
        senha,
        tipo,
      });
      setUsuarios([...usuarios, response.data]);
      setNome("");
      setEmail("");
      setSenha("");
      setTipo("cliente");
      setErro("");
      setSucesso("Usuário criado com sucesso!");
    } catch (err) {
      setErro("Erro ao adicionar usuário");
      setSucesso("");
    }
  };

  return (
    <div className="usuarios-container">
      <h2>Usuários</h2>

      {/* ✅ Formulário completo com todos os campos do backend */}
      <div className="form-usuario">
        <input
          type="text"
          placeholder="Nome"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Senha"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
        />
        <select value={tipo} onChange={(e) => setTipo(e.target.value)}>
          <option value="cliente">Cliente</option>
          <option value="atendente">Atendente</option>
        </select>
        <button onClick={adicionarUsuario}>Adicionar</button>
      </div>

      {erro && <p className="erro">{erro}</p>}
      {sucesso && <p className="sucesso">{sucesso}</p>}

      <ul>
        {usuarios.map((u, index) => (
          // ✅ Usa index como fallback caso não venha id do backend
          <li key={u.id || index}>{u.nome} — {u.email} ({u.tipo})</li>
        ))}
      </ul>
    </div>
  );
}

export default Usuarios;
