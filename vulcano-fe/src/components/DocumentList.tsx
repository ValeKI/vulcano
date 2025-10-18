import React from 'react';
import DocumentItem from './DocumentItem';

interface DocumentListProps {
    listFiles?: string[];
}

const DocumentList: React.FC<DocumentListProps> = ({ listFiles = [] }) => {
    
    const onViewFile = (fileName: string) => {
        console.log(`Viewing file: ${fileName}`);
    }

    const onDownloadFile = (fileName: string) => {
        console.log(`Downloading file: ${fileName}`);
    }

    return (
        <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
            {listFiles.map((file, idx) => (
                <li key={idx}>
                    <DocumentItem name={file} onView={() => onViewFile(file)} onDownload={() => onDownloadFile(file)} selected={idx === 3} />
                </li>
            ))}
        </ul>
    );
}

export default DocumentList;