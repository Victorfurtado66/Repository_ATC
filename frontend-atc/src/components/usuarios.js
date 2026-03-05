import React, { useState } from "react";
import api from "../api";
import "./usuario.css";

function Usuarios() {
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [tipo, setTipo] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post("/usuarios/", {
    nome,
    email,
    senha,
    tipo,
  });
    console.log("Resposta do backend:", response.data);
    alert(`Usuário cadastrado com sucesso! Email: ${response.data.email}`);
  }
  catch (err) {
    if (err.response) {
      console.log("Erro completo:", err.response.data);
      alert(`Erro: ${JSON.stringify(err.response.data)}`);
    } else {
      console.log("Erro inesperado:", err);
      alert(`Erro completo: ${JSON.stringify(err.response.data)}`);
    }
  }
  };

  return (
    <div className="usuarios-container">
      <h2>Cadastrar Usuário</h2>
      <form onSubmit={handleSubmit}>
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
          <option value="">Selecione o tipo</option>
          <option value="cliente">Cliente</option>
          <option value="atendente">Atendente</option>
        </select>
        <button type="submit">Cadastrar</button>
      </form>
    </div>
  );
}

export default Usuarios;