import React, { useState } from 'react';
import DocumentList from '../components/DocumentList';
import ChatInput from '../components/ChatInput';
import ChatResponse from '../components/ChatResponse';
import AnswerList from '../components/AnswerList';
import VulcanoPage from './VulcanoPage';
import { getUserFiles } from '../services/FileService';
import { type DocumentListFile } from '../components/DocumentList';


const Chat: React.FC = () => {
  const [listDocuments, setListDocuments] = useState<DocumentListFile[]>([]);
  const handlePdfSelect = async (file: File | null) => {
    if (file) {
      try {
        const res = await getUserFiles();
        const mappedFiles: DocumentListFile[] = res.files.map(f => ({
          ...f,
          selectByAnswer: false
        }));
        setListDocuments(mappedFiles);
      } catch (e) {
        alert("Errore nel recupero dei file utente:");
        console.error(e);
      }
    }
  };


  return (
    <VulcanoPage>
      <div className="chatbox-container">
        <div className="chatbox-left">
          <DocumentList listFiles={listDocuments} />
        </div>
        <div className="chatbox-center">
          <div className="chatbox-responsewindow">
            <ChatResponse text="Example response text" />
          </div>
          <div className="chatbox-chatwindow">
            <ChatInput onHandlePdfSelect={handlePdfSelect} />
          </div>
        </div>
        <div className="chatbox-right">
          <AnswerList />
        </div>
      </div>
    </VulcanoPage>
  );
}

export default Chat;