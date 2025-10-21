import React, { useState, useEffect } from 'react';
import DocumentList from '../components/DocumentList';
import ChatInput from '../components/ChatInput';
import ChatResponse from '../components/ChatResponse';
import QuestionList from '../components/QuestionList';
import VulcanoPage from './VulcanoPage';
import { getUserFiles } from '../services/FileService';
import { type DocumentListFile } from '../components/DocumentList';
import { type Question } from '../services/ChatService';
import { getQuestionsByUserId, type GetQuestionsByUserIdResponse, type InsertQuestionResponse } from '../api/ChatApi';
import { getFilesByAnswerId } from '../services/FileService';
import { getAnswerByQuestionId } from '../services/ChatService';
import PdfViewer from '../components/PdfViewer';


const Chat: React.FC = () => {
  const [listDocuments, setListDocuments] = useState<DocumentListFile[]>([]);
  const [listQuestions, setListQuestions] = useState<Question[]>([]);
  const [answer, setAnswer] = useState<string>("");
  const [question, setQuestion] = useState<string>("");
  const [viewPdfFile, setViewPdfFile] = useState<Blob | null>(null);
  const [selectedQuestionId, setSelectedQuestionId] = useState<number | null>(null);

  // Carica i file e le domande all'ingresso nella pagina
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const filesRes = await getUserFiles();
        const mappedFiles: DocumentListFile[] = filesRes.files.map(f => ({
          ...f
        }));
        setListDocuments(mappedFiles);

        const questionsRes: GetQuestionsByUserIdResponse = await getQuestionsByUserId();
        // Ordina per id crescente
        const sortedQuestions = [...questionsRes.questions].sort((a, b) => a.id - b.id);
        setListQuestions(sortedQuestions);
        if (sortedQuestions.length > 0) {
          handleViewQuestion(sortedQuestions[sortedQuestions.length - 1].id);
        }
      } catch (e) {
        console.error("Errore nel caricamento iniziale:", e);
      }
    };
    fetchInitialData();
  }, []);

  const handlePdfSelect = async (file: File | null) => {
    if (file) {
      try {
        const res = await getUserFiles();
        const mappedFiles: DocumentListFile[] = res.files.map(f => ({
          ...f
        }));
        setListDocuments(mappedFiles);
      } catch (e) {
        alert("Errore nel recupero dei file utente:");
        console.error(e);
      }
    }
  };

  const handleViewQuestion = async (questionId: number) => {
    try {
      const questionRes = await getQuestionsByUserId();
      const question = questionRes.questions.find(q => q.id === questionId);
      const answerRes = await getAnswerByQuestionId(questionId);
      console.log("Answer ID:", answerRes.id);
      const file_ids = await getFilesByAnswerId(answerRes.id).then(res => res.files.map(f => f.file_id));

      console.log("File IDs associati alla risposta:", file_ids);

      if (question && answerRes) {
        setQuestion(question.content);
        setAnswer(answerRes.content);
        setSelectedQuestionId(questionId);

        setListDocuments(prevDocs =>
          prevDocs.map(doc => ({
            ...doc,
            selectByAnswer: file_ids?.includes(doc.file_id) ?? false
          }))
        );
      }
    } catch (e) {
      console.error("Errore nel recupero della domanda:", e);
    }
  };

  const handleQuestionSubmit = async ({ id, question, answer, file_ids }: InsertQuestionResponse) => {
    const res: GetQuestionsByUserIdResponse = await getQuestionsByUserId();

    // Fix: usa optional chaining per evitare errori se answer non è un oggetto
    const answerText = (answer && typeof answer === "object" && "answer" in answer)
      ? (answer as any).answer
      : answer;

    setAnswer(answerText);
    setQuestion(question);
    console.log("handleQuestionSubmit - Submitted Question ID:", id);
    setSelectedQuestionId(id);

    // Ordina per id crescente
    const sortedQuestions = [...res.questions].sort((a, b) => a.id - b.id);
    setListQuestions(sortedQuestions);

    setListDocuments(prevDocs =>
      prevDocs.map(doc => ({
        ...doc,
        selectByAnswer: file_ids?.includes(doc.file_id) ?? false
      }))
    );
  };

  const closePdfViewer = () => {
    setViewPdfFile(null);
  };

  
  const handlePdfSelectView = (file: Blob) => {
    setViewPdfFile(file);
  };

  return (
    <VulcanoPage>
      <div className="chatbox-container">
        <div className="chatbox-left">
          <DocumentList listFiles={listDocuments} handleOnViewFile={handlePdfSelectView} />
        </div>
        <div className="chatbox-center">
          <div className="chatbox-responsewindow">
            <ChatResponse questionText={question} answerText={answer} />
          </div>
          <div className="chatbox-chatwindow">
            <ChatInput onHandlePdfSelect={handlePdfSelect} onQuestionSubmit={handleQuestionSubmit}/>
          </div>
        </div>
        <div className="chatbox-right">
          <QuestionList questionList={listQuestions} onViewQuestion={handleViewQuestion} selectedQuestionId={selectedQuestionId} />
        </div>
      </div>

      {viewPdfFile && (
        <div
          className="pdf-viewer-overlay"
          onClick={closePdfViewer}
          style={{ cursor: 'pointer' }}
        >
          <div
            className="pdf-viewer-modal"
            onClick={e => e.stopPropagation()}
          >
            <PdfViewer file={viewPdfFile as Blob} onClose={closePdfViewer}/>
          </div>
        </div>
      )}
    </VulcanoPage>
  );
}

export default Chat;