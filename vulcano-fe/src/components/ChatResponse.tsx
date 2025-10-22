interface DocumentItemProps { questionText?: string, answerText?: string }

const ChatResponse: React.FC<DocumentItemProps> = ({ questionText, answerText }) => {
    return (
        <div className="response-window-content">
            <div className="response-label">
                Domanda:
            </div>
            <div className="response-question">
                {questionText}
            </div>
            <div className="response-label">
                Risposta:
            </div>
            <div className="response-answer">
                {answerText}
            </div>
        </div>
    );
}

export default ChatResponse;