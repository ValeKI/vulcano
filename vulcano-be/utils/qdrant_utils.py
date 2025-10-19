from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
import uuid
from config import CURRENT_CONFIG
from io import BytesIO
import PyPDF2
from utils.db.db_file_utils import get_file_by_id

def upload_file_chunks_to_qdrant(user_id, file_id, file_name, file_content, chunk_size=1024, collection_name="files"):
    print(f"[QDRANT] upload_file_chunks_to_qdrant: user_id={user_id}, file_id={file_id}, file_name={file_name}")
    client = QdrantClient(host=CURRENT_CONFIG.QDRANT_HOST, port=CURRENT_CONFIG.QDRANT_PORT, timeout=30.0)
    collections = [c.name for c in client.get_collections().collections]
    print(f"[QDRANT] Existing collections: {collections}")
    if collection_name not in collections:
        print(f"[QDRANT] Creating collection: {collection_name}")
        client.create_collection(
            collection_name=collection_name,
            vectors_config={"size": 1, "distance": "Cosine"}
        )
    if hasattr(file_content, "read"):
        print("[QDRANT] Reading file_content from file-like object")
        file_content = file_content.read()
    if file_name and file_name.lower().endswith(".pdf"):
        print("[QDRANT] Extracting text from PDF")
        file_content = extract_pdf_text(file_content)
        print(f"[QDRANT] PDF text length: {len(file_content)}")
    if isinstance(file_content, bytes):
        print("[QDRANT] Decoding file_content from bytes to string")
        file_content = file_content.decode("utf-8", errors="replace")
    print(f"[QDRANT] Content length: {len(file_content)}")
    chunks = [file_content[i:i+chunk_size] for i in range(0, len(file_content), chunk_size)]
    print(f"[QDRANT] Chunks to upload: {len(chunks)}")
    if not chunks:
        print("[QDRANT] No chunks to upload (file vuoto?)")
        return 0
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
    batch_size = 1000
    for i in range(0, len(points), batch_size):
        print(f"[QDRANT] Upserting batch {i//batch_size+1} ({i}:{i+batch_size})")
        client.upsert(collection_name=collection_name, points=points[i:i+batch_size])
    print(f"[QDRANT] Uploaded {len(points)} chunks for file_id={file_id}")
    return len(points)

def get_file_ids_by_answer_id(answer_id, collection_name="files"):
    print(f"[QDRANT] get_file_ids_by_answer_id: {answer_id}")
    client = QdrantClient(host=CURRENT_CONFIG.QDRANT_HOST, port=CURRENT_CONFIG.QDRANT_PORT, timeout=30.0)
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
    print(f"[QDRANT] Found file_ids: {list(file_ids)}")
    return list(file_ids)

def get_file_ids_by_user_id(user_id, collection_name="files"):
    print(f"[QDRANT] get_file_ids_by_user_id: {user_id}")
    client = QdrantClient(host=CURRENT_CONFIG.QDRANT_HOST, port=CURRENT_CONFIG.QDRANT_PORT, timeout=30.0)
    query = {
        "must": [
            {
                "key": "user_id",
                "match": {"value": user_id}
            }
        ]
    }
    results = client.scroll(collection_name=collection_name, scroll_filter=query, limit=1000)
    file_ids = set()
    for point in results[0]:
        file_ids.add(point.payload["file_id"])
    print(f"[QDRANT] Found file_ids: {list(file_ids)}")
    return list(file_ids)

def extract_pdf_text(file_content):
    print("[QDRANT] extract_pdf_text")
    if isinstance(file_content, BytesIO):
        pdf_stream = file_content
    else:
        pdf_stream = BytesIO(file_content)
    reader = PyPDF2.PdfReader(pdf_stream)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        print(f"[QDRANT] Extracted {len(page_text)} chars from page")
        text += page_text
    print(f"[QDRANT] Total extracted text length: {len(text)}")
    return text

def add_answer_id_to_file_chunks(file_id, answer_id, collection_name="files"):
    """
    Aggiorna tutti i chunk di un file su Qdrant aggiungendo l'answer_id in answer_ids.
    """
    print(f"[QDRANT] add_answer_id_to_file_chunks: file_id={file_id}, answer_id={answer_id}")
    client = QdrantClient(host=CURRENT_CONFIG.QDRANT_HOST, port=CURRENT_CONFIG.QDRANT_PORT, timeout=30.0)
    query = {
        "must": [
            {
                "key": "file_id",
                "match": {"value": file_id}
            }
        ]
    }
    results = client.scroll(collection_name=collection_name, scroll_filter=query, limit=1000)
    points_to_update = []
    for point in results[0]:
        payload = point.payload
        answer_ids = payload.get("answer_ids", [])
        if answer_id not in answer_ids:
            answer_ids.append(answer_id)
            payload["answer_ids"] = answer_ids
            # Assicurati che il vettore sia una lista di float (es: [0.0])
            vector = getattr(point, "vector", None)
            if vector is None:
                vector = [0.0]
            points_to_update.append(PointStruct(id=point.id, vector=vector, payload=payload))
    if points_to_update:
        client.upsert(collection_name=collection_name, points=points_to_update)
        print(f"[QDRANT] Updated {len(points_to_update)} chunks for file_id={file_id} with answer_id={answer_id}")
    else:
        print(f"[QDRANT] No chunks to update for file_id={file_id}")
    return len(points_to_update)