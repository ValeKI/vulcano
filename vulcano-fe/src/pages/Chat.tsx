import React, { useState } from 'react';
import DocumentList from '../components/DocumentList';
import ChatInput from '../components/ChatInput';
import ChatResponse from '../components/ChatResponse';
import QuestionList from '../components/QuestionList';
import VulcanoPage from './VulcanoPage';
import { getUserFiles } from '../services/FileService';
import { type DocumentListFile } from '../components/DocumentList';
import { type Question } from '../services/ChatService';
import { getQuestionsByUserId, type GetQuestionsByUserIdResponse, type InsertQuestionResponse } from '../api/ChatApi';


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

  const [listQuestions, setListQuestions] = useState<Question[]>([]);

  const [answer, setAnswer] = useState<string>("");
  const [question, setQuestion] = useState<Question | null>(null);
  const handleQuestionSubmit = async ({ question, answer, file_ids }: InsertQuestionResponse) => {
    const res: GetQuestionsByUserIdResponse = await getQuestionsByUserId();
    setAnswer(answer);
    setQuestion(question);
    setListQuestions(res.questions);

    console.log("file attuali:", listDocuments);
    console.log("file_ids ricevuti:", file_ids);

    setListDocuments(prevDocs =>
      prevDocs.map(doc => ({
        ...doc,
        selectByAnswer: file_ids?.includes(doc.file_id) ?? false
      }))
    );
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
            <ChatInput onHandlePdfSelect={handlePdfSelect} onQuestionSubmit={handleQuestionSubmit}/>
          </div>
        </div>
        <div className="chatbox-right">
          <QuestionList questionList={listQuestions}/>
        </div>
      </div>
    </VulcanoPage>
  );
}

export default Chat;