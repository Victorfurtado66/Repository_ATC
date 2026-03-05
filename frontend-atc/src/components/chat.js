import React, { useState, useEffect } from "react";
import api from "../api";

function Chat({ ticketId }) {
  const [mensagens, setMensagens] = useState([]);
  const [conteudo, setConteudo] = useState("");

  useEffect(() => {
    const fetchMensagens = async () => {
      const token = localStorage.getItem("token");
      const response = await api.get(`/mensagens/${ticketId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMensagens(response.data);
    };
    fetchMensagens();
  }, [ticketId]);

  const enviarMensagem = async () => {
    const token = localStorage.getItem("token");
    await api.post(
      `/mensagens/${ticketId}`,
      { conteudo },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    setConteudo("");
    // Atualiza lista
    const response = await api.get(`/mensagens/${ticketId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    setMensagens(response.data);
  };

  return (
    <div className="chat-container">
      <h3>Chat do Ticket #{ticketId}</h3>
      <div className="chat-mensagens">
        {mensagens.map((m) => (
          <p key={m.id}>
            <strong>{m.remetente} ({m.tipo}):</strong> {m.conteudo}
          </p>
        ))}
      </div>
      <input
        type="text"
        placeholder="Digite sua mensagem..."
        value={conteudo}
        onChange={(e) => setConteudo(e.target.value)}
      />
      <button onClick={enviarMensagem}>Enviar</button>
    </div>
  );
}

export default Chat;