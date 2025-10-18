import React, { useRef, useState } from "react";
import '../styles/main.scss';

interface PdfFileDropProps {
  onFileSelect: (file: File | null) => void;
  loadingPercent?: number;
}

const PdfFileDrop: React.FC<PdfFileDropProps> = ({ onFileSelect, loadingPercent = 0 }) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [errorUpload, setErrorUpload] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = (file: File | null) => {
    if (file && file.type === "application/pdf") {
      setErrorUpload(null);
      setSelectedFile(file);
      onFileSelect(file);
    } else {
      setErrorUpload("Per favore carica un file PDF valido.");
      setSelectedFile(null);
      onFileSelect(null);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null;
    handleFile(file);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragActive(false);
    const file = e.dataTransfer.files?.[0] || null;
    handleFile(file);
  };

  return (
    <div
      className={`pdf-file-drop${dragActive ? " drag-active" : ""}`}
      onDragOver={e => { e.preventDefault(); setDragActive(true); }}
      onDragLeave={e => { e.preventDefault(); setDragActive(false); }}
      onDrop={handleDrop}
      onClick={() => fileInputRef.current?.click()}
      title="Trascina qui un PDF o clicca per selezionare"
    >
      <input
        type="file"
        accept="application/pdf"
        className="pdf-file-drop-input"
        ref={fileInputRef}
        onChange={handleChange}
        tabIndex={-1}
      />
      <span role="img" aria-label="allega">📎</span>
      <span>
        {loadingPercent > 0 ? (
          <span className="pdf-file-drop__loading">
            Caricamento... {loadingPercent}%
          </span>
        ) : selectedFile ? (
          <span className="pdf-file-drop__filename">{selectedFile.name}</span>
        ) : errorUpload ? (
          <span className="pdf-file-drop__error">{errorUpload}</span>
        ) : (
          <span className="pdf-file-drop__placeholder">
            Trascina o clicca per PDF
          </span>
        )}
      </span>
    </div>
  );
};

export default PdfFileDrop;
