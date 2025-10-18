import React, { useState } from "react";
import PdfFileDrop from "./PdfFileDrop";

const ChatInput: React.FC = () => {
    const [input, setInput] = useState("");
    const [pdfFile, setPdfFile] = useState<File | null>(null);
    const [showPdfDrop, setShowPdfDrop] = useState(false);
    const [loadingPercent, setLoadingPercent] = useState<number>(0);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (input.trim()) {
            console.log("Domanda inviata:", input);
            if (pdfFile) {
                console.log("PDF allegato:", pdfFile.name);
            }
            setInput("");
            setPdfFile(null);
            setShowPdfDrop(false);
            setLoadingPercent(0);
        }
    };

    const handlePdfSelect = async (file: File | null) => {
        if (file) {
            setLoadingPercent(1);
            // Simula caricamento con percentuale
            for (let i = 1; i <= 100; i += 5) {
                await new Promise((res) => setTimeout(res, 20));
                setLoadingPercent(i);
            }
            console.log("PDF selezionato:", file.name);
            setPdfFile(file);
            setShowPdfDrop(false);
            setLoadingPercent(0);
        }
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
                    onClick={() => {
                        setShowPdfDrop((prev) => !prev);
                        setPdfFile(null);
                        setLoadingPercent(0);
                    }}
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
                        <PdfFileDrop
                            onFileSelect={handlePdfSelect}
                            loadingPercent={loadingPercent}
                        />
                    </div>
                </div>
            )}
        </form>
    );
};

export default ChatInput;