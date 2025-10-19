import React, { useEffect } from 'react';
import DocumentItem from './DocumentItem';

export interface DocumentListFile {
    file_id: number;
    file_name: string;
    format: string;
    user_id?: number;
    selectByAnswer?: boolean;
}

interface DocumentListProps {
    listFiles?: DocumentListFile[];
}

const DocumentList: React.FC<DocumentListProps> = ({ listFiles = [] }) => {
    useEffect(() => {
        console.log('listFiles aggiornato:', listFiles);
    }, [listFiles]);

    const onViewFile = (fileName: string) => {
        console.log(`Viewing file: ${fileName}`);
    }

    const onDownloadFile = (fileName: string) => {
        console.log(`Downloading file: ${fileName}`);
    }

    return (
        <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
            {listFiles.map((file) => (
                <li key={file.file_id}>
                    <DocumentItem
                        name={file.file_name}
                        onView={() => onViewFile(file.file_name)}
                        onDownload={() => onDownloadFile(file.file_name)}
                        selected={!!file.selectByAnswer}
                    />
                </li>
            ))}
        </ul>
    );
}

export default DocumentList;