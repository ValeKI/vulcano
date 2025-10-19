import React, { useState } from "react";
import PdfFileDrop from "./PdfFileDrop";
import { uploadFile } from "../api/FileApi";

const ChatInput: React.FC = () => {
    const [input, setInput] = useState("");
    const [pdfFile, setPdfFile] = useState<File | null>(null);
    const [showPdfDrop, setShowPdfDrop] = useState(false);
    const [loadingPercent, setLoadingPercent] = useState<number>(0);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        // Invia solo la domanda, mai il PDF
        if (input.trim()) {
            console.log("Domanda inviata:", input);
            setInput("");
        }
    };

    const handlePdfSelect = async (file: File | null) => {
        if (file) {
            setLoadingPercent(1);
            let percent = 1;
            let completed = false;
            let error = false;

            // Timer per timeout di 2 minuti
            const timeout = setTimeout(() => {
                setLoadingPercent(0);
                setPdfFile(null);
                setShowPdfDrop(false);
                error = true;
                alert("Errore: caricamento file troppo lento o fallito.");
            }, 2 * 60 * 1000);

            // Simula avanzamento percentuale fino al 98%
            const progressInterval = setInterval(() => {
                if (percent < 98 && !completed && !error) {
                    percent += 2;
                    setLoadingPercent(percent);
                }
            }, 400); // 400ms * 49 = ~20s

            try {
                await uploadFile({ file });
                completed = true;
                clearTimeout(timeout);
                clearInterval(progressInterval);
                setLoadingPercent(100);
                setTimeout(() => setLoadingPercent(0), 500);
                setPdfFile(null);
                setShowPdfDrop(false);
            } catch (e) {
                clearTimeout(timeout);
                clearInterval(progressInterval);
                setLoadingPercent(0);
                setPdfFile(null);
                setShowPdfDrop(false);
                alert("Errore durante il caricamento del file.");
            }
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