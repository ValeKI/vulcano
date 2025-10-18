import React from 'react';
import DocumentList from '../components/DocumentList';
import ChatInput from '../components/ChatInput';
import ChatResponse from '../components/ChatResponse';
import AnswerList from '../components/AnswerList';
import VulcanoPage from './VulcanoPage';

const Chat: React.FC = () => (
  <VulcanoPage>
  <div className="chatbox-container">
    <div className="chatbox-left">
      <DocumentList />
    </div>
    <div className="chatbox-center">
      <div className="chatbox-responsewindow">
        <ChatResponse text="Example response text" />
      </div>
      <div className="chatbox-chatwindow">
        <ChatInput />
      </div>
    </div>
    <div className="chatbox-right">
      <AnswerList />
    </div>
  </div>
  </VulcanoPage>
);

export default Chat;