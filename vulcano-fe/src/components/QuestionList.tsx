import React from "react";
import ItemView from "./DocumentItem";
import type { Question } from "../services/ChatService";

interface QuestionListProps {
    questionList?: Question[];
    onViewQuestion: (questionId: number) => void;
}

const QuestionList: React.FC<QuestionListProps> = ({ questionList = [], onViewQuestion }) => {
    const handleViewQuestion = (questionId: number) => {
        onViewQuestion(questionId);
    }

    return (
        <ul>
            {questionList.map((question, idx) => (
                <ItemView key={question.id} name={`Domanda ${idx + 1}`} onView={() => handleViewQuestion(question.id)} type="question" />
            ))}
        </ul>
    );
}

export default QuestionList;