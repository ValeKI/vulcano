import React, { useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { authApi } from "../api/AuthApi";
import VulcanoPage from "./VulcanoPage";
import "../styles/main.scss";

const ResetPassword: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get("token") || "";
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!password || !confirm) {
      setError("Inserisci la nuova password e la conferma.");
      return;
    }
    if (password !== confirm) {
      setError("Le password non coincidono.");
      return;
    }
    if (!token) {
      setError("Token mancante.");
      return;
    }

    setLoading(true);
    try {
      await authApi.resetPassword({
        token,
        new_password: password,
      });
      setSuccess(true);
      setTimeout(() => navigate("/"), 2000);
    } catch (err: any) {
      setError(
        err?.response?.data?.error ||
        "Errore durante il reset della password."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <VulcanoPage>
        
    <div className="login">
    <div className="loginbox">
        
          <div className="box">
      <h2>Reset Password</h2>
      {success ? (
        <div className="success-message">
          Password aggiornata con successo! Reindirizzamento...
        </div>
      ) : (
        <form onSubmit={handleSubmit}>
          <div>
            <input
             className="user-input"
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
              placeholder="Nuova password"
            />
          </div>
          <div>
            <input
             className="user-input"
              type="password"
              value={confirm}
              onChange={e => setConfirm(e.target.value)}
              required
              placeholder="Conferma password"
            />
          </div>
          {error && <div className="error-message">{error}</div>}
          <button className="login-btn" type="submit" disabled={loading}>
            {loading ? "Attendi..." : "Resetta Password"}
          </button>
          <button
            type="button"
            className="forgot-btn"
            style={{ marginTop: "0.5rem" }}
            onClick={() => navigate("/")}
          >
            Indietro
          </button>
        </form>
      )}
    </div>
    </div></div>
    </VulcanoPage>
  );
};

export default ResetPassword;
