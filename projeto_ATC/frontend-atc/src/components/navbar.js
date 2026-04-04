import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "./navbar.css";

function Navbar() {
  const navigate = useNavigate();
  // ✅ Verifica se está logado
  const token = localStorage.getItem("token");

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <h1>ATC System</h1>
      <ul>
        {/* ✅ Se não está logado, mostra só Login */}
        {!token ? (
          <li><Link to="/login">Login</Link></li>
        ) : (
          // ✅ Se está logado, mostra navegação e botão Sair
          <>
            <li><Link to="/tickets">Tickets</Link></li>
            <li><Link to="/usuarios">Usuários</Link></li>
            <li>
              <button onClick={handleLogout} className="logout-btn">
                Sair
              </button>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
}

export default Navbar;
