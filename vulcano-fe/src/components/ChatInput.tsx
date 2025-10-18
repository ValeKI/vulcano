import React, { useState } from "react";
import PdfFileDrop from "./PdfFileDrop";

const ChatInput: React.FC = () => {
    const [input, setInput] = useState("");
    const [pdfFile, setPdfFile] = useState<File | null>(null);
    const [showPdfDrop, setShowPdfDrop] = useState(false);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (input.trim()) {
            console.log("Domanda inviata:", input);
            if (pdfFile) {
                console.log("PDF allegato:", pdfFile.name);
            }
            setInput("");
            setPdfFile(null);
            setShowPdfDrop(false);
        }
    };

    const handleTogglePdfDrop = () => {
        setShowPdfDrop((prev) => !prev);
        if (showPdfDrop) setPdfFile(null);
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="chat-window-form chat-input-form"
        >
            <div className="chat-input-row">
                <button
                    type="button"
                    className={`chat-input-togglepdf${
                        showPdfDrop ? " active" : ""
                    }`}
                    onClick={handleTogglePdfDrop}
                    aria-label={showPdfDrop ? "Nascondi PDF" : "Allega PDF"}
                >
                    {showPdfDrop ? "−" : "+"}
                </button>
                <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Scrivi la tua domanda..."
                    className="chat-window"
                    rows={2}
                    wrap="soft"
                />
                <button type="submit">Invia</button>
            </div>
            {showPdfDrop && (
                <div className="chat-input-pdfdrop">
                    <div className="chat-input-pdfdrop-inner">
                        <PdfFileDrop onFileSelect={setPdfFile} />
                    </div>
                </div>
            )}
        </form>
    );
};

export default ChatInput;