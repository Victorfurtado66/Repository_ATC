import React from "react";
import { Link } from "react-router-dom";
import "./navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <h1>ATC System</h1>
      <ul>
        <li><Link to="/login">Login</Link></li>
        <li><Link to="/tickets">Tickets</Link></li>
        <li><Link to="/usuarios">Usuários</Link></li>
      </ul>
    </nav>
  );
}

export default Navbar;