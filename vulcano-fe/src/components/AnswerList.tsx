import React from "react";
import ItemView from "./DocumentItem";

const AnswerList: React.FC = () => {
    const listAnswers = Array.from({ length: 500 }, (_, i) => `Answer ${i + 1}`);

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