import React, { useEffect, useState } from "react";
import api from "../api";
import "./usuario.css";

function Usuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const [nome, setNome] = useState("");

  useEffect(() => {
    const fetchUsuarios = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await api.get("/usuarios", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setUsuarios(response.data);
      } catch (err) {
        console.error("Erro ao carregar usuários", err);
      }
    };
    fetchUsuarios();
  }, []);

  const adicionarUsuario = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await api.post(
        "/usuarios",
        { nome },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setUsuarios([...usuarios, response.data]);
      setNome("");
    } catch (err) {
      console.error("Erro ao adicionar usuário", err);
    }
  };

  return (
    <div className="usuarios-container">
      <h2>Usuários</h2>
      <ul>
        {usuarios.map((u) => (
          <li key={u.id}>{u.nome}</li>
        ))}
      </ul>
      <input
        type="text"
        placeholder="Novo usuário"
        value={nome}
        onChange={(e) => setNome(e.target.value)}
      />
      <button onClick={adicionarUsuario}>Adicionar</button>
    </div>
  );
}

export default Usuarios;