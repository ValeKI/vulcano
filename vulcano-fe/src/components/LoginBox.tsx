import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/main.scss";
import { LoginService } from "../services/LoginService";
import { useAuth } from "../context/AuthContext";
import SignUpBox from "../components/SignUpBox";

const LoginBox: React.FC = () => {
  const [usernameOrEmail, setUsernameOrEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [showSignUp, setShowSignUp] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const token = await LoginService.login({ usernameOrEmail, password });

      login(token);

    } catch (err: any) {
      console.error("Login failed:", err);
      setError(typeof err === "string" ? err : "Credenziali non valide");
    } finally {
      setLoading(false);
    }
  };

  if (showSignUp) {
    return <SignUpBox onBack={() => setShowSignUp(false)} />;
  }

  return (
    <div className="loginbox">
      <div className="box">
        <h2>Accedi</h2>

        <form onSubmit={handleLogin}>
          <input
            type="text"
            placeholder="Email o username"
            value={usernameOrEmail}
            onChange={(e) => setUsernameOrEmail(e.target.value)}
            className="user-input"
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="user-input"
          />

          <button type="submit" disabled={loading}>
            {loading ? "Accesso..." : "Login"}
          </button>
        </form>

        {error && <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>}

        <button type="button" className="forgot-btn">
          Password dimenticata?
        </button>

        <button
          type="button"
          className="forgot-btn"
          style={{ marginTop: "0.5rem" }}
          onClick={() => setShowSignUp(true)}
        >
          Registrati
        </button>
      </div>
    </div>
  );
};

export default LoginBox;
