import base64
import redis
import json
from config import CURRENT_CONFIG


class RedisUtils:
    def __init__(self, host=None, port=None, db=None):
        host = host if host is not None else CURRENT_CONFIG.REDIS_HOST
        port = port if port is not None else CURRENT_CONFIG.REDIS_PORT
        db = db if db is not None else CURRENT_CONFIG.REDIS_DB
        print(f"[REDIS] Connecting to Redis at {host}:{port}, db={db}")
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    def get_key_redis_cache(self, user_id, content):
        encoded_content = base64.b64encode(content.encode()).decode()
        key = f"question_{user_id}_{encoded_content}"
        print(f"[REDIS] Generated cache key: {key}")
        return key

    def read_from_redis_cache(self, user_id, content):
        key = self.get_key_redis_cache(user_id, content)
        print(f"[REDIS] Reading from cache with key: {key}")
        return self._read_from_redis_cache(key)

    def _read_from_redis_cache(self, key):
        resp = self.redis_client.hgetall(key)
        print(f"[REDIS] Cache read for key {key}: {resp}")
        if not resp:
            print(f"[REDIS] No cache found for key: {key}")
            return None
        result = {
            "answer": resp.get(b"answer").decode() if resp.get(b"answer") else "",
            "file_ids": json.loads(resp.get(b"file_ids").decode()) if resp.get(b"file_ids") else [],
            "question_id": int(resp.get(b"question_id").decode()) if resp.get(b"question_id") else None,
            "answer_id": int(resp.get(b"answer_id").decode()) if resp.get(b"answer_id") else None
        }
        print(f"[REDIS] Decoded cache result: {result}")
        return result

    def write_to_redis_cache(self, user_id, content, answer, file_ids, question_id=None, answer_id=None):
        key = self.get_key_redis_cache(user_id, content)
        value = {
            "answer": answer["answer"] if isinstance(answer, dict) and "answer" in answer else answer,
            "file_ids": json.dumps(file_ids),
            "question_id": str(question_id) if question_id is not None else "",
            "answer_id": str(answer_id) if answer_id is not None else ""
        }
        print(f"[REDIS] Writing to cache key: {key} value: {value}")
        self.redis_client.hset(key, mapping=value)
        print(f"[REDIS] Write complete for key: {key}")
