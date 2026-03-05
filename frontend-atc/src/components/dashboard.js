import React, { useEffect, useState } from "react";
import api from "../api";
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";

function Dashboard() {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    const fetchMetrics = async () => {
      const token = localStorage.getItem("token");
      const response = await api.get("/dashboard", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMetrics(response.data);
    };
    fetchMetrics();
  }, []);

  if (!metrics) return <p>Carregando métricas...</p>;

  const prioridadeData = Object.entries(metrics.tickets_por_prioridade).map(
    ([key, value]) => ({ name: key, value })
  );

  return (
    <div className="dashboard-container">
      <h2>Dashboard</h2>
      <p>Tickets abertos: {metrics.tickets_abertos}</p>
      <p>Tickets fechados: {metrics.tickets_fechados}</p>
      <p>Tempo médio de resposta: {metrics.tempo_medio_resposta_horas} horas</p>

      <h3>Tickets por prioridade</h3>
      <PieChart width={400} height={300}>
        <Pie
          data={prioridadeData}
          dataKey="value"
          nameKey="name"
          cx="50%"
          cy="50%"
          outerRadius={100}
        >
          {prioridadeData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={["#0088FE", "#00C49F", "#FFBB28"][index]} />
          ))}
        </Pie>
        <Tooltip />
      </PieChart>
    </div>
  );
}

export default Dashboard;