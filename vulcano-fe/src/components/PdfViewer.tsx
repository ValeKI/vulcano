import React, { useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;
interface PdfViewerProps {
  file: Blob | string;
  onClose: () => void;
}

const PdfViewer: React.FC<PdfViewerProps> = ({ file, onClose }) => {
  const [numPages, setNumPages] = useState<number>(1);
  const [pageNumber, setPageNumber] = useState<number>(1);
  const [zoom, setZoom] = useState<number>(Math.min(window.innerWidth * 0.75, 70 * 16));

  const handleZoomIn = () => setZoom(z => Math.min(z + 100, window.innerWidth * 0.9));
  const handleZoomOut = () => setZoom(z => Math.max(z - 100, 300));
  const handlePageChange = (n: number) => setPageNumber(n);

  return (
    <div className="pdf-viewer-modal">
      <div className="pdf-viewer-controls">
        <span className="pdf-viewer-page-label">
          Pagina:
          <input
            type="number"
            min={1}
            max={numPages}
            value={pageNumber}
            onChange={e => handlePageChange(Number(e.target.value))}
            className="pdf-viewer-page-input"
          />
          / {numPages}
        </span>
        
        <button className="pdf-viewer-zoom-btn" onClick={handleZoomOut}>-</button>
        <button className="pdf-viewer-zoom-btn" onClick={handleZoomIn}>+</button>
       
         <button
          onClick={onClose}
          className="pdf-viewer-close-btn"
        >
          Chiudi
        </button>
      </div>
      <div className="pdf-viewer-content">
        <Document file={file} onLoadSuccess={({ numPages }) => setNumPages(numPages)}>
          <div style={{ marginBottom: '1.7rem', display: 'flex', justifyContent: 'center' }}>
            <Page
              pageNumber={pageNumber}
              renderTextLayer={false}
              renderAnnotationLayer={false}
              width={zoom}
            />
          </div>
        </Document>
      </div>
    </div>
  );
};

export default PdfViewer;
