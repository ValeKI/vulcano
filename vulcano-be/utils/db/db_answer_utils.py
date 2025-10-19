from db import get_cursor
from typing import Optional, Dict

def insert_answer(question_id: int, content: str) -> int:

    cur = get_cursor()
    cur.execute(
        "INSERT INTO answers (question_id, content) VALUES (%s, %s) RETURNING id",
        (question_id, content)
    )
    answer_id = cur.fetchone()['id']
    cur.connection.commit()
    return answer_id

def get_answer_by_question_id(question_id: int) -> Optional[Dict]:
    cur = get_cursor()
    cur.execute(
        "SELECT id, question_id, content, content_file_id, created_at FROM answers WHERE question_id=%s",
        (question_id,)
    )
    row = cur.fetchone()
    if row:
        return {
            "id": row['id'],
            "question_id": row['question_id'],
            "content": row['content'],
            "content_file_id": row['content_file_id'],
            "created_at": row['created_at']
        }
    return None
