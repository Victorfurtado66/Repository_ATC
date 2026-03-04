import axios from "axios";

// Configuração da instância Axios
const api = axios.create({
  baseURL: "http://localhost:8000", // URL do backend FastAPI
});

// Interceptador para adicionar o token JWT automaticamente
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;