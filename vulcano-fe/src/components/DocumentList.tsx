import React from 'react';
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

    const onViewFile = (file_id: number) => {
    }

    const onDownloadFile = (file_id: number) => {
    }

    return (
        <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
            {listFiles.map((file) => (
                <li key={file.file_id}>
                    <DocumentItem
                        name={file.file_name}
                        onView={() => onViewFile(file.file_id)}
                        onDownload={() => onDownloadFile(file.file_id)}
                        selected={!!file.selectByAnswer}
                    />
                </li>
            ))}
        </ul>
    );
}

export default DocumentList;