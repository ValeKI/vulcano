import base64
import redis
import json


redis_client = redis.Redis(host='localhost', port=6379, db=0)


def get_key_redis_cache(user_id, content):
    encoded_content = base64.b64encode(content.encode()).decode()
    return f"question_{user_id}_{encoded_content}"


def read_from_redis_cache(user_id, content):
    key = get_key_redis_cache(user_id, content)
    return _read_from_redis_cache(key)


def _read_from_redis_cache(key):
    resp = redis_client.hgetall(key)
    if not resp:
        return None
    return {
        "answer": resp.get(b"answer").decode() if resp.get(b"answer") else "",
        "file_ids": json.loads(resp.get(b"file_ids").decode()) if resp.get(b"file_ids") else [],
        "question_id": int(resp.get(b"question_id").decode()) if resp.get(b"question_id") else None,
        "answer_id": int(resp.get(b"answer_id").decode()) if resp.get(b"answer_id") else None
    }


def write_to_redis_cache(user_id, content, answer, file_ids, question_id=None, answer_id=None):
    key = get_key_redis_cache(user_id, content)
    value = {
        "answer": answer["answer"] if isinstance(answer, dict) and "answer" in answer else answer,
        "file_ids": json.dumps(file_ids),
        "question_id": str(question_id) if question_id is not None else "",
        "answer_id": str(answer_id) if answer_id is not None else ""
    }
    redis_client.hset(key, mapping=value)
