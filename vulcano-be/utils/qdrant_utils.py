from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
import uuid
from config import CURRENT_CONFIG

def upload_file_chunks_to_qdrant(user_id, file_id, file_content, chunk_size=1024, collection_name="files"):
    client = QdrantClient(host=CURRENT_CONFIG.QDRANT_HOST, port=CURRENT_CONFIG.QDRANT_PORT)
    # Check if collection exists, create if not
    if collection_name not in [c.name for c in client.get_collections().collections]:
        client.create_collection(
            collection_name=collection_name,
            vectors_config={"size": 1, "distance": "Cosine"}
        )
    chunks = [file_content[i:i+chunk_size] for i in range(0, len(file_content), chunk_size)]
    points = []
    for idx, chunk in enumerate(chunks):
        point_id = str(uuid.uuid4())
        payload = {
            "user_id": user_id,
            "file_id": file_id,
            "chunk_index": idx,
            "content": chunk,
            "answer_ids": []
        }
        points.append(PointStruct(id=point_id, vector=[0.0], payload=payload))
    client.upsert(collection_name=collection_name, points=points)
    return len(points)

def get_file_ids_by_answer_id(answer_id, collection_name="files"):
    client = QdrantClient(host=CURRENT_CONFIG.QDRANT_HOST, port=CURRENT_CONFIG.QDRANT_PORT)
    query = {
        "must": [
            {
                "key": "answer_ids",
                "match": {"value": answer_id}
            }
        ]
    }
    results = client.scroll(collection_name=collection_name, scroll_filter=query, limit=1000)
    file_ids = set()
    for point in results[0]:
        file_ids.add(point.payload["file_id"])
    return list(file_ids)
