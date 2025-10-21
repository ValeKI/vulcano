from db import get_cursor
from typing import Optional, List, Dict

class DbQuestionUtils:
    def get_question_by_id(self, question_id: int) -> Optional[Dict]:
        print(f"[DB] get_question_by_id: {question_id}")
        cur = get_cursor()
        cur.execute(
            "SELECT id, content, user_id, content_file_id, created_at FROM questions WHERE id=%s",
            (question_id,)
        )
        row = cur.fetchone()
        print(f"[DB] Question fetched: {row if row else None}")
        return {
            "id": row[0],
            "content": row[1],
            "user_id": row[2],
            "content_file_id": row[3],
            "created_at": row[4]
        } if row else None

    def list_questions_by_user_id(self, user_id: int) -> List[Dict]:
        print(f"[DB] list_questions_by_user_id: {user_id}")
        cur = get_cursor()
        cur.execute(
            "SELECT id, content, user_id, content_file_id, created_at FROM questions WHERE user_id=%s ORDER BY created_at DESC",
            (user_id,)
        )
        rows = cur.fetchall()
        print(f"[DB] Questions fetched: {rows}")
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

    def insert_question(self, user_id: int, content: str) -> int:
        print(f"[DB] insert_question: user_id={user_id}, content={content}")
        cur = get_cursor()
        cur.execute(
            "INSERT INTO questions (user_id, content) VALUES (%s, %s) RETURNING id",
            (user_id, content)
        )
        question_id = cur.fetchone()['id']
        cur.connection.commit()
        print(f"[DB] Question inserted with id: {question_id}")
        return question_id
