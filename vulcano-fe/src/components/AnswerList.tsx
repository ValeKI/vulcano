import React from "react";
import ItemView from "./DocumentItem";

interface AnswerListProps {
    listAnswers?: string[];
}

const AnswerList: React.FC<AnswerListProps> = ({ listAnswers = [] }) => {
    const onViewAnswer = (fileName: string) => {
        console.log(`Viewing file: ${fileName}`);
    }

    return (
        <ul>
            {listAnswers.map((answer, idx) => (
                <ItemView key={idx} name={answer} onView={() => onViewAnswer(answer)} type="answer" />
            ))}
        </ul>
    );
}

export default AnswerList;