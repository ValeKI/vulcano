
interface DocumentItemProps { text: string }

const ChatResponse: React.FC<DocumentItemProps> = ({ text }) => {
    return (
        <div className="response-window-content">
            <p>
                {text}    
            </p>
        </div>
    );
}

export default ChatResponse;