import React, { useState } from "react";
import "../styles/main.scss";
import { authApi } from "../api/AuthApi";

interface ForgotPasswordBoxProps {
  onBack: () => void;
}

const ForgotPasswordBox: React.FC<ForgotPasswordBoxProps> = ({ onBack }) => {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleForgot = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await authApi.forgotPassword({ email });
      setSent(true);
    } catch (err: any) {
      setError(
        err?.response?.data?.error ||
        "Errore durante l'invio dell'email di recupero."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="loginbox">
      <div className="box">
        <h2>Recupera password</h2>
        {sent ? (
          <div style={{ color: "green", marginTop: "1rem" }}>
            Se l'email è registrata riceverai un link per il reset.
          </div>
        ) : (
          <form onSubmit={handleForgot}>
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              className="user-input"
              required
            />
            <button type="submit" disabled={loading}>
              {loading ? "Invio..." : "Invia link di reset"}
            </button>
          </form>
        )}
        {error && <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>}
        <button
          type="button"
          className="forgot-btn"
          style={{ marginTop: "0.5rem" }}
          onClick={onBack}
        >
          Indietro
        </button>
      </div>
    </div>
  );
};

export default ForgotPasswordBox;
