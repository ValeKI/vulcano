import React, { useRef, useState } from "react";
import '../styles/main.scss';

interface PdfFileDropProps {
  onFileSelect: (file: File | null) => void;
}

const PdfFileDrop: React.FC<PdfFileDropProps> = ({ onFileSelect }) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = (file: File | null) => {
    if (file && file.type === "application/pdf") {
      setSelectedFile(file);
      onFileSelect(file);
    } else {
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
      {selectedFile ? (
        <span className="pdf-file-drop__filename">{selectedFile.name}</span>
      ) : (
        <span className="pdf-file-drop__placeholder">
          Trascina o clicca per PDF
        </span>
      )}
    </div>
  );
};

export default PdfFileDrop;
