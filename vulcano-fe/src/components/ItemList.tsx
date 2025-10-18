import React from 'react';
import ListItem from './ListItem';

const ItemList: React.FC = () => {
    const listFiles = Array.from({ length: 500 }, (_, i) => `File${i + 1}.txt`);

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
                    <ListItem name={file} onView={() => onViewFile(file)} onDownload={() => onDownloadFile(file)} selected={idx === 3} />
                </li>
            ))}
        </ul>
    );
}

export default ItemList;