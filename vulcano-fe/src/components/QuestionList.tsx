import React, { useEffect } from "react";
import ItemView from "./DocumentItem";
import type { Question } from "../services/ChatService";

interface QuestionListProps {
    questionList?: Question[];
}

const QuestionList: React.FC<QuestionListProps> = ({ questionList = [] }) => {
   useEffect(() => {
        console.log('questionList aggiornato:', questionList);
    }, [questionList]);

    const onViewAnswer = (questionId: number) => {
        console.log(`Viewing question: ${questionId}`);
    }

    return (
        <ul>
            {questionList.map((answer, idx) => (
                <ItemView key={answer.id} name={`Question ${idx + 1}`} onView={() => onViewAnswer(answer.id)} type="question" />
            ))}
        </ul>
    );
}

export default QuestionList;