import React, { useEffect, useState } from "react";
import api from "../api";

function Historico() {
  const [tickets, setTickets] = useState([]);

  useEffect(() => {
    const fetchHistorico = async () => {
      const token = localStorage.getItem("token");
      const response = await api.get("/historico", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTickets(response.data);
    };
    fetchHistorico();
  }, []);

  return (
    <div className="historico-container">
      <h2>Histórico de Atendimentos</h2>
      <ul>
        {tickets.map((t) => (
          <li key={t.id}>
            <strong>{t.titulo}</strong> - {t.descricao} <br />
            Prioridade: {t.prioridade} <br />
            Criado em: {new Date(t.data_criacao).toLocaleString()} <br />
            Fechado em: {new Date(t.data_fechamento).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Historico;