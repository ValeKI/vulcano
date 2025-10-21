import React from "react";
import ItemView from "./DocumentItem";
import type { Question } from "../services/ChatService";

interface QuestionListProps {
    questionList?: Question[];
    onViewQuestion: (questionId: number) => void;
    selectedQuestionId?: number | null;
}

const QuestionList: React.FC<QuestionListProps> = ({ questionList = [], onViewQuestion, selectedQuestionId }) => {
    const [selectedId, setSelectedId] = React.useState<number | null>(selectedQuestionId || null);
    const handleViewQuestion = (questionId: number) => {
        onViewQuestion(questionId);
        setSelectedId(questionId);
    }

    return (
        <ul>
            {questionList.map((question, idx) => (
                <ItemView key={question.id} name={`Domanda ${idx + 1}`} selected={selectedId === question.id} onView={() => handleViewQuestion(question.id)} type="question" />
            ))}
        </ul>
    );
}

export default QuestionList;