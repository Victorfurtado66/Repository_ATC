import React, { useEffect, useState } from "react";
import api from "../api";
import "./tickets.css";

function Tickets() {
  const [tickets, setTickets] = useState([]);
  const [titulo, setTitulo] = useState("");
  const [descricao, setDescricao] = useState("");
  const [prioridade, setPrioridade] = useState("baixa");
  const [erro, setErro] = useState("");
  const [sucesso, setSucesso] = useState("");

  useEffect(() => {
    const fetchTickets = async () => {
      try {
        // ✅ Token removido, já é tratado pelo interceptador
        const response = await api.get("/tickets");
        setTickets(response.data);
      } catch (err) {
        console.error("Erro ao carregar tickets", err);
      }
    };
    fetchTickets();
  }, []);

  const adicionarTicket = async () => {
    if (!titulo || !descricao) {
      setErro("Preencha título e descrição!");
      return;
    }
    try {
      // ✅ Envia todos os campos que o backend exige
      const response = await api.post("/tickets", {
        cliente_id: 1, // idealmente pegar do token JWT decodificado
        titulo,
        descricao,
        status: "aberto",
        prioridade,
      });
      setTickets([...tickets, response.data]);
      setTitulo("");
      setDescricao("");
      setPrioridade("baixa");
      setErro("");
      setSucesso("Ticket criado com sucesso!");
    } catch (err) {
      setErro("Erro ao adicionar ticket");
      setSucesso("");
    }
  };

  return (
    <div className="tickets-container">
      <h2>Tickets</h2>

      {/* ✅ Formulário completo */}
      <div className="form-ticket">
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
        <button onClick={adicionarTicket}>Adicionar Ticket</button>
      </div>

      {erro && <p className="erro">{erro}</p>}
      {sucesso && <p className="sucesso">{sucesso}</p>}

      <ul>
        {tickets.map((ticket, index) => (
          <li key={ticket.id || index}>
            <strong>{ticket.titulo}</strong> — {ticket.status} — Prioridade: {ticket.prioridade}
            <p>{ticket.descricao}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Tickets;
