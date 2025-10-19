import React, { useState } from "react";
import "../styles/main.scss";
import { authApi } from "../api/AuthApi";


const SignUpBox: React.FC<{ onBack: () => void }> = ({ onBack }) => {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const validateEmail = (email: string) =>
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

    const handleSignUp = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError(null);
        setSuccess(null);

        if (!username.trim()) {
            setError("Username obbligatorio");
            return;
        }
        if (!validateEmail(email)) {
            setError("Email non valida");
            return;
        }
        if (password.length < 4) {
            setError("La password deve avere almeno 4 caratteri");
            return;
        }
        if (password !== confirmPassword) {
            setError("Le password non coincidono");
            return;
        }

        setLoading(true);
        try {
            await authApi.signUp({username, email, password});
            setSuccess("Registrazione avvenuta con successo!");
            onBack();
        } catch (err: any) {
            setError("Errore durante la registrazione");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="loginbox">
            <div className="box">
                <h2>Registrati</h2>
                <form onSubmit={handleSignUp}>
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className="user-input"
                    />
                    <input
                        type="text"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="user-input"
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="user-input"
                    />
                    <input
                        type="password"
                        placeholder="Conferma password"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        className="user-input"
                    />
                    <button type="submit" disabled={loading}>
                        {loading ? "Registrazione..." : "Conferma"}
                    </button>
                </form>
                {error && <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>}
                {success && (
                    <p style={{ color: "green", marginTop: "1rem" }}>{success}</p>
                )}
                <button type="button" className="forgot-btn" onClick={onBack}>
                    Torna al login
                </button>
            </div>
        </div>
    );
};

export default SignUpBox;