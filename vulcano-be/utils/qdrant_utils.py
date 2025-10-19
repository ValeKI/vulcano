from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
import uuid
from config import CURRENT_CONFIG
from io import BytesIO
import PyPDF2

def upload_file_chunks_to_qdrant(user_id, file_id, file_name, file_content, chunk_size=1024, collection_name="files", file_name=None):
    client = QdrantClient(
        host=CURRENT_CONFIG.QDRANT_HOST,
        port=CURRENT_CONFIG.QDRANT_PORT,
        timeout=300.0
    )
    # Check if collection exists, create if not
    if collection_name not in [c.name for c in client.get_collections().collections]:
        client.create_collection(
            collection_name=collection_name,
            vectors_config={"size": 1, "distance": "Cosine"}
        )
    # Se file_content è file-like, leggilo
    if hasattr(file_content, "read"):
        file_content = file_content.read()
    # Se il file è un PDF, estrai il testo
    if file_name and file_name.lower().endswith(".pdf"):
        file_content = extract_pdf_text(file_content)
        print(file_content)  # Se qui vedi caratteri strani, il problema è nel PDF
    # Se file_content è bytes, decodifica in stringa
    if isinstance(file_content, bytes):
        file_content = file_content.decode("utf-8", errors="replace")
    chunks = [file_content[i:i+chunk_size] for i in range(0, len(file_content), chunk_size)]
    if not chunks:
        return 0
    points = []
    for idx, chunk in enumerate(chunks):
        point_id = str(uuid.uuid4())
        payload = {
            "user_id": user_id,
            "file_id": file_id,
            "chunk_index": idx,
            "content": chunk,  # chunk effettivo del file
            "answer_ids": []
        }
        points.append(PointStruct(id=point_id, vector=[0.0], payload=payload))
    # Invia i punti in batch per evitare il limite di payload
    batch_size = 1000
    for i in range(0, len(points), batch_size):
        client.upsert(collection_name=collection_name, points=points[i:i+batch_size])
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

def get_file_ids_by_user_id(user_id, collection_name="files"):
    client = QdrantClient(host=CURRENT_CONFIG.QDRANT_HOST, port=CURRENT_CONFIG.QDRANT_PORT)
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
    return list(file_ids)

def extract_pdf_text(file_content):
    reader = PyPDF2.PdfReader(BytesIO(file_content))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text