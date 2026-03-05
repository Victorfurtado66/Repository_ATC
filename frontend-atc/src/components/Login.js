import React, { useState } from "react";
import api from "../api"; // axios configurado
import "./login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // O backend espera form-data (não JSON)
      const params = new URLSearchParams();
      params.append("username", email);
      params.append("password", senha);

      const response = await api.post("/auth/login", params);

      // Salva o token JWT
      localStorage.setItem("token", response.data.access_token);

      // Redireciona para Tickets
      window.location.href = "/tickets";
    } catch (err) {
      setErro("Usuário ou senha inválidos");
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Digite seu e-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Digite sua senha"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
        />
        <button type="submit">Entrar</button>
      </form>
      {erro && <p className="erro">{erro}</p>}
    </div>
  );
}

export default Login;