import React from 'react';
import ItemList from '../components/ItemList';
import ChatInput from '../components/ChatInput';
import ChatResponse from '../components/ChatResponse';
import AnswerList from '../components/AnswerList';

const Chat: React.FC = () => (
  <div className="chatbox-container">
    <div className="chatbox-left">
      <ItemList />
    </div>
    <div className="chatbox-center">
      <div className="chatbox-responsewindow">
        <ChatResponse />
      </div>
      <div className="chatbox-chatwindow">
        <ChatInput />
      </div>
    </div>
    <div className="chatbox-right">
      <AnswerList />
    </div>
  </div>
);

export default Chat;