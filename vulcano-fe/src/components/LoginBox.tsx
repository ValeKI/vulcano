import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import '../styles/main.scss';
import { LoginService } from "../services/LoginService";


const LoginBox: React.FC = () => {
  const [usernameOrEmail, setusernameOrEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const success = await LoginService.login({ usernameOrEmail, password });
      if (success) {
        navigate("/chat");
      }
    } catch (err: any) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="loginbox">
      <div className="box">
        <h2>Accedi</h2>

        <form onSubmit={handleLogin}>
          <input
            type="text"
            placeholder="Email o username"
            value={usernameOrEmail}
            onChange={(e) => setusernameOrEmail(e.target.value)}
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
      </div>
    </div>
  );
};


export default LoginBox;
