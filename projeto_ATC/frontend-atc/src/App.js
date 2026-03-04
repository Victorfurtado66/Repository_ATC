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
        {/* Rota pública */}
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />

        {/* Rotas protegidas */}
        <Route
          path="/tickets"
          element={
            <PrivateRoute>
              <Tickets />
            </PrivateRoute>
          }
        />
        <Route
          path="/usuarios"
          element={
            <PrivateRoute>
              <Usuarios />
            </PrivateRoute>
          }
        />
      </Routes>
    </Router>
  );
}


export default App;