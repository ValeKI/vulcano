import base64
import redis
import json


class RedisUtils:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    def get_key_redis_cache(self, user_id, content):
        encoded_content = base64.b64encode(content.encode()).decode()
        return f"question_{user_id}_{encoded_content}"

    def read_from_redis_cache(self, user_id, content):
        key = self.get_key_redis_cache(user_id, content)
        return self._read_from_redis_cache(key)

    def _read_from_redis_cache(self, key):
        resp = self.redis_client.hgetall(key)
        if not resp:
            return None
        return {
            "answer": resp.get(b"answer").decode() if resp.get(b"answer") else "",
            "file_ids": json.loads(resp.get(b"file_ids").decode()) if resp.get(b"file_ids") else [],
            "question_id": int(resp.get(b"question_id").decode()) if resp.get(b"question_id") else None,
            "answer_id": int(resp.get(b"answer_id").decode()) if resp.get(b"answer_id") else None
        }

    def write_to_redis_cache(self, user_id, content, answer, file_ids, question_id=None, answer_id=None):
        key = self.get_key_redis_cache(user_id, content)
        value = {
            "answer": answer["answer"] if isinstance(answer, dict) and "answer" in answer else answer,
            "file_ids": json.dumps(file_ids),
            "question_id": str(question_id) if question_id is not None else "",
            "answer_id": str(answer_id) if answer_id is not None else ""
        }
        self.redis_client.hset(key, mapping=value)
