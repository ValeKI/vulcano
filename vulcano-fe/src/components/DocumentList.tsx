import React from 'react';
import DocumentItem from './DocumentItem';
import { downloadFile } from '../services/FileService';

export interface DocumentListFile {
    file_id: number;
    file_name: string;
    format: string;
    user_id?: number;
    selectByAnswer?: boolean;
}

interface DocumentListProps {
    listFiles?: DocumentListFile[];
    handleOnViewFile?: (file: Blob) => void;
}

const DocumentList: React.FC<DocumentListProps> = ({ listFiles = [], handleOnViewFile }) => {

    const onViewFile = async (file_id: number) => {
        const blob = await downloadFile(file_id);
       
        handleOnViewFile && handleOnViewFile(blob);
    }

    const onDownloadFile = async (file_name: string, file_id: number) => {
        const blob = await downloadFile(file_id);
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = file_name;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    }

    return (
        <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
            {listFiles.map((file) => (
                <li key={file.file_id}>
                    <DocumentItem
                        name={file.file_name}
                        onView={() => onViewFile(file.file_id)}
                        onDownload={() => onDownloadFile(file.file_name, file.file_id)}
                        selected={!!file.selectByAnswer}
                    />
                </li>
            ))}
        </ul>
    );
}

export default DocumentList;