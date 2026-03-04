import React, { useEffect, useState } from "react";
import api from "../api";
import "./tickets.css";

function Tickets() {
  const [tickets, setTickets] = useState([]);

  useEffect(() => {
    const fetchTickets = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await api.get("/tickets", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setTickets(response.data);
      } catch (err) {
        console.error("Erro ao carregar tickets", err);
      }
    };
    fetchTickets();
  }, []);

  // ✅ Agora as funções estão dentro do componente
  const adicionarTicket = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await api.post(
        "/tickets",
        { titulo: "Novo ticket", status: "aberto" },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setTickets([...tickets, response.data]);
    } catch (err) {
      console.error("Erro ao adicionar ticket", err);
    }
  };

  const removerTicket = async (id) => {
    try {
      const token = localStorage.getItem("token");
      await api.delete(`/tickets/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTickets(tickets.filter((t) => t.id !== id));
    } catch (err) {
      console.error("Erro ao remover ticket", err);
    }
  };

  return (
    <div className="tickets-container">
      <h2>Tickets</h2>
      <button onClick={adicionarTicket}>Adicionar Ticket</button>
      <ul>
        {tickets.map((ticket) => (
          <li key={ticket.id}>
            <strong>{ticket.titulo}</strong> - {ticket.status}
            <button onClick={() => removerTicket(ticket.id)}>Remover</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Tickets;