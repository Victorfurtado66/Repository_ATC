import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./components/Login";
import Tickets from "./components/tickets";
import Usuarios from "./components/usuarios";
import Navbar from "./components/navbar";
import PrivateRoute from "./components/privateRoute";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        {/* Rotas públicas */}
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/usuarios" element={<Usuarios />} /> {/* CADASTRO LIVRE */}

        {/* Rotas protegidas */}
        <Route
          path="/tickets"
          element={
            <PrivateRoute>
              <Tickets />
            </PrivateRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;