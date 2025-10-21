from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, Filter, FieldCondition
from io import BytesIO
import PyPDF2
import tempfile
import os
from datapizza.embedders.openai import OpenAIEmbedder
from datapizza.vectorstores.qdrant import QdrantVectorstore
from datapizza.clients.openai import OpenAIClient
from datapizza.pipeline import DagPipeline
from datapizza.modules.rewriters import ToolRewriter
from datapizza.modules.prompt import ChatPromptTemplate
from datapizza.core.vectorstore import VectorConfig
from datapizza.embedders import ChunkEmbedder
from datapizza.modules.parsers.docling import DoclingParser
from datapizza.modules.parsers.text_parser import TextParser
from datapizza.modules.splitters import NodeSplitter
from datapizza.pipeline import IngestionPipeline
from config import CURRENT_CONFIG
from utils.ai_utils import embedder, vectorstore

class QdrantUtils:
    def upload_file_chunks_to_qdrant(self, user_id, file_id, file_name, file_content, chunk_size=10000, collection_name=None):
        print(f"[QDRANT] Uploading file chunks: user_id={user_id}, file_id={file_id}, file_name={file_name}")
        if collection_name is None:
            collection_name = CURRENT_CONFIG.QDRANT_COLLECTION_NAME
        pipeline = IngestionPipeline(
            modules=[
                TextParser(),
                NodeSplitter(max_char=chunk_size),
                embedder,
            ],
            vector_store=vectorstore,
            collection_name=collection_name
        )
        # with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_name)[-1]) as tmp_file:
        #     tmp_file.write(file_content)
        #     tmp_file_path = tmp_file.name
        try:
            pipeline.run(self.extract_pdf_text(file_content), metadata={"file_id": file_id, "user_id": user_id})
            print(f"[QDRANT] Ingestion pipeline completed for file: {file_name}")
        except Exception as e:
            print(f"[QDRANT] Error during ingestion pipeline: {e}")
            return 0

    def get_file_ids_by_answer_id(self, answer_id, collection_name=None):
        print(f"[QDRANT] get_file_ids_by_answer_id called with answer_id={answer_id}")
        if collection_name is None:
            collection_name = CURRENT_CONFIG.QDRANT_COLLECTION_NAME
        print(f"[QDRANT] get_file_ids_by_answer_id: {answer_id}")
        try:
            answer_id = int(answer_id)
        except Exception:
            print(f"[QDRANT] Warning: answer_id non convertibile a int: {answer_id}")
        client = QdrantClient(host=CURRENT_CONFIG.QDRANT_HOST, port=CURRENT_CONFIG.QDRANT_PORT, timeout=30.0)
        q_filter = Filter(
            must=[
                FieldCondition(
                    key="answer_ids",
                    match={"value": answer_id}
                )
            ]
        )
        all_points = []
        next_page_offset = None
        while True:
            results = client.scroll(collection_name=collection_name, scroll_filter=q_filter, offset=next_page_offset, limit=1000)
            points = results[0]
            print(f"[QDRANT] Retrieved {len(points)} points in this page for answer_id={answer_id}")
            all_points.extend(points)
            next_page_offset = results[1]
            if not next_page_offset:
                break
        print(f"[QDRANT] Total points retrieved for answer_id={answer_id}: {len(all_points)}")
        file_ids = set()
        for point in all_points:
            file_ids.add(point.payload["file_id"])
        print(f"[QDRANT] Found file_ids: {list(file_ids)}")
        return list(file_ids)

    def get_file_ids_by_user_id(self, user_id, collection_name=None):
        print(f"[QDRANT] get_file_ids_by_user_id called with user_id={user_id}")
        if collection_name is None:
            collection_name = CURRENT_CONFIG.QDRANT_COLLECTION_NAME
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
        all_points = []
        next_page_offset = None
        while True:
            results = client.scroll(collection_name=collection_name, scroll_filter=query, offset=next_page_offset)
            points = results[0]
            print(f"[QDRANT] Retrieved {len(points)} points in this page")
            all_points.extend(points)
            next_page_offset = results[1]
            if not next_page_offset:
                break
        print(f"[QDRANT] Total points retrieved: {len(all_points)}")
        file_ids = set()
        for point in all_points:
            file_ids.add(point.payload["file_id"])
        print(f"[QDRANT] Found file_ids: {list(file_ids)}")
        return list(file_ids)

    def extract_pdf_text(self, file_content):
        print("[QDRANT] extract_pdf_text called")
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

    def add_answer_id_to_file_chunks(self, file_id, answer_id, collection_name="files"):
        print(f"[QDRANT] add_answer_id_to_file_chunks called: file_id={file_id}, answer_id={answer_id}, collection_name={collection_name}")
        if collection_name is None:
            collection_name = CURRENT_CONFIG.QDRANT_COLLECTION_NAME
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
        all_points = []
        next_page_offset = None
        while True:
            results = client.scroll(collection_name=collection_name, scroll_filter=query, offset=next_page_offset, limit=1000)
            points = results[0]
            print(f"[QDRANT] Retrieved {len(points)} points in this page for file_id={file_id}")
            all_points.extend(points)
            next_page_offset = results[1]
            if not next_page_offset:
                break
        print(f"[QDRANT] Total points retrieved for file_id={file_id}: {len(all_points)}")

        updated_count = 0
        for point in all_points:
            payload = point.payload
            answer_ids = payload.get("answer_ids", [])
            if answer_id not in answer_ids:
                answer_ids.append(answer_id)
                payload["answer_ids"] = answer_ids
                print(f"[QDRANT] Updating payload for point.id={point.id}")
                client.set_payload(collection_name=collection_name, payload=payload, points=[point.id])
                updated_count += 1
        if updated_count:
            print(f"[QDRANT] Updated {updated_count} chunks for file_id={file_id} with answer_id={answer_id}")
        else:
            print(f"[QDRANT] No chunks to update for file_id={file_id}")
        return updated_count
    
    def extract_pdf_text(self, file_content):
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