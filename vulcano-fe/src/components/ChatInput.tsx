import React, { useState } from "react";

const ChatInput: React.FC = () => {
    const [input, setInput] = useState("");

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (input.trim()) {
            console.log("Domanda inviata:", input);
            setInput("");
        }
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="chat-window-form"
        >
            <textarea
                value={input}
                onChange={e => setInput(e.target.value)}
                placeholder="Scrivi la tua domanda..."
                className="chat-window"
                rows={2}
                wrap="soft"
            />
            <button type="submit">Invia</button>
        </form>
    );
};

export default ChatInput;