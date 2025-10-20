import React, { useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;
interface PdfViewerProps {
  file: Blob | string;
  onClose: () => void;
}

const PdfViewer: React.FC<PdfViewerProps> = ({ file, onClose }) => {
  const [numPages, setNumPages] = useState<number>(1);

  return (
    <div className="pdf-viewer-modal">
      <button onClick={onClose}>Chiudi</button>
      <Document file={file} onLoadSuccess={({ numPages }) => setNumPages(numPages)}>
        {Array.from({ length: numPages }, (_, idx) => (
          <Page key={idx + 1} pageNumber={idx + 1} />
        ))}
      </Document>
    </div>
  );
};

export default PdfViewer;
