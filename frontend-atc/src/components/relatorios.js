import React from "react";
import api from "../api";

function Relatorios() {
  const baixarCSV = async () => {
    const token = localStorage.getItem("token");
    const response = await api.get("/relatorios/tickets_csv", {
      headers: { Authorization: `Bearer ${token}` },
      responseType: "blob",
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "relatorio_tickets.csv");
    document.body.appendChild(link);
    link.click();
  };

  return (
    <div className="relatorios-container">
      <h2>Relatórios</h2>
      <button onClick={baixarCSV}>Exportar Tickets (CSV)</button>
    </div>
  );
}

export default Relatorios;