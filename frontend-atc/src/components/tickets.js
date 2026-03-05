import React, { useEffect, useState } from "react";
import api from "../api";
import "./tickets.css";

function Tickets() {
  const [tickets, setTickets] = useState([]);
  const [titulo, setTitulo] = useState("");
  const [descricao, setDescricao] = useState("");
  const [prioridade, setPrioridade] = useState("media");

  useEffect(() => {
    const fetchTickets = async () => {
      const token = localStorage.getItem("token");
      const response = await api.get("/tickets", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTickets(response.data);
    };
    fetchTickets();
  }, []);

  const criarTicket = async () => {
    const token = localStorage.getItem("token");
    await api.post(
      "/tickets",
      { titulo, descricao, prioridade },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    alert("Ticket criado!");
  };

  return (
    <div className="tickets-container">
      <h2>Tickets</h2>
      <form onSubmit={(e) => { e.preventDefault(); criarTicket(); }}>
        <input
          type="text"
          placeholder="Título"
          value={titulo}
          onChange={(e) => setTitulo(e.target.value)}
        />
        <textarea
          placeholder="Descrição"
          value={descricao}
          onChange={(e) => setDescricao(e.target.value)}
        />
        <select value={prioridade} onChange={(e) => setPrioridade(e.target.value)}>
          <option value="baixa">Baixa</option>
          <option value="media">Média</option>
          <option value="alta">Alta</option>
        </select>
        <button type="submit">Abrir Ticket</button>
      </form>

      <ul>
        {tickets.map((t) => (
          <li key={t.id}>
            <strong>{t.titulo}</strong> - {t.status} ({t.prioridade})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Tickets;