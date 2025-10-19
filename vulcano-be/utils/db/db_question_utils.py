from db import get_cursor
from typing import Optional, List, Dict

def get_question_by_id(question_id: int) -> Optional[Dict]:
    cur = get_cursor()
    cur.execute(
        "SELECT id, content, user_id, content_file_id, created_at FROM questions WHERE id=%s",
        (question_id,)
    )
    row = cur.fetchone()
    if row:
        return {
            "id": row[0],
            "content": row[1],
            "user_id": row[2],
            "content_file_id": row[3],
            "created_at": row[4]
        }
    return None

def list_questions_by_user_id(user_id: int) -> List[Dict]:
    cur = get_cursor()
    cur.execute(
        "SELECT id, content, user_id, content_file_id, created_at FROM questions WHERE user_id=%s ORDER BY created_at DESC",
        (user_id,)
    )
    rows = cur.fetchall()
    return [
        {
            "id": row['id'],
            "content": row['content'],
            "user_id": row['user_id'],
            "content_file_id": row['content_file_id'],
            "created_at": row['created_at']
        }
        for row in rows
    ]

def insert_question(user_id: int, content: str) -> int:
    cur = get_cursor()
    cur.execute(
        "INSERT INTO questions (user_id, content) VALUES (%s, %s) RETURNING id",
        (user_id, content)
    )
    question_id = cur.fetchone()['id']
    cur.connection.commit()
    return question_id
