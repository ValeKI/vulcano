import random
import re
from datapizza.embedders.openai import OpenAIEmbedder
from datapizza.vectorstores.qdrant import QdrantVectorstore
from datapizza.clients.openai import OpenAIClient
from datapizza.pipeline import DagPipeline
from datapizza.modules.rewriters import ToolRewriter
from datapizza.modules.prompt import ChatPromptTemplate
from datapizza.core.vectorstore import VectorConfig
from datapizza.embedders import ChunkEmbedder
from datapizza.modules.parsers.docling import DoclingParser
from datapizza.modules.splitters import NodeSplitter
from datapizza.pipeline import IngestionPipeline
from config import CURRENT_CONFIG

openai_client = OpenAIClient(
    model="gpt-4o-mini",
    api_key=CURRENT_CONFIG.OPENAI_API_KEY
)
vectorstore = QdrantVectorstore(host="localhost", port=6333)
EMBEDDING_MODEL = CURRENT_CONFIG.EMBEDDING_MODEL
EMBEDDING_DIM = CURRENT_CONFIG.EMBEDDING_DIM
chatEmbedder = OpenAIEmbedder(api_key=CURRENT_CONFIG.OPENAI_API_KEY, model_name=EMBEDDING_MODEL)
embedder = ChunkEmbedder(client=chatEmbedder)
vectorstore.create_collection(CURRENT_CONFIG.QDRANT_COLLECTION_NAME, vector_config=[VectorConfig(name="embedding", dimensions=EMBEDDING_DIM)])
emb = OpenAIEmbedder(api_key=CURRENT_CONFIG.OPENAI_API_KEY, model_name=EMBEDDING_MODEL)

def call_ai_to_generate_answer_mock(question, file_list):
    print("[AI] file_list ricevuti:", file_list)
    risposta = f"Risposta generata per la domanda: {question}"
    sampled_files = random.sample(file_list, min(2, len(file_list)))
    print("[AI] sampled_files scelti:", sampled_files)
    file_ids = [file['file_id'] for file in sampled_files]
    print("[AI] file_ids estratti:", file_ids)
    return {
        "answer": risposta,
        "file_ids": file_ids
    }

def call_ai_to_generate_answer(question, user_id=None):
    dag_pipeline = DagPipeline()
    dag_pipeline.add_module("rewriter", ToolRewriter(
        client=openai_client,
        system_prompt=CURRENT_CONFIG.REWRITER_SYSTEM_PROMPT
    ))
    dag_pipeline.add_module("embedder", emb)
    # Aggiungi filtro per user_id se disponibile
    retriever_kwargs = {
        "collection_name": CURRENT_CONFIG.QDRANT_COLLECTION_NAME,
        "k": 5
    }
    if user_id is not None:
        retriever_kwargs["filter"] = {"must": [{"key": "user_id", "match": {"value": user_id}}]}
    dag_pipeline.add_module("retriever", vectorstore.as_retriever(**retriever_kwargs))
    dag_pipeline.add_module("prompt", ChatPromptTemplate(
        user_prompt_template="",
        retrieval_prompt_template=CURRENT_CONFIG.RETRIEVAL_PROMPT_TEMPLATE
    ))

    openai_client.system_prompt = CURRENT_CONFIG.GENERATOR_SYSTEM_PROMPT
    dag_pipeline.add_module("generator", openai_client)
    dag_pipeline.connect("rewriter", "embedder", target_key="text")
    dag_pipeline.connect("embedder", "retriever", target_key="query_vector")
    dag_pipeline.connect("retriever", "prompt", target_key="chunks")
    dag_pipeline.connect("prompt", "generator", target_key="memory")

    query = question

    result = dag_pipeline.run({
        "rewriter": {"user_prompt": query},
        "prompt": {"user_prompt": query},
        "retriever": {
            "collection_name": CURRENT_CONFIG.QDRANT_COLLECTION_NAME,
            "k": 3
        },
        "generator": {"input": query}
    })

    response_text = None
    if result is not None and 'generator' in result and getattr(result['generator'], 'text', None) is not None:
        response_text = result['generator'].text
    else:
        response_text = "Nessuna risposta generata. (Errore: risposta nulla)"

    return {
        "answer": extract_answer_text(response_text),
        "file_ids": extract_file_ids_from_response(response_text)
    }

def extract_file_ids_from_response(response: str):
    """
    Estrae un array di ID da una stringa tipo 'FILE_UTILIZZATI[1, 2]: ...'
    """
    match = re.search(r'FILE_UTILIZZATI\[(.*?)\]', response)
    if not match:
        return []
    ids_str = match.group(1)
    ids = [int(x.strip()) for x in ids_str.split(',') if x.strip().isdigit()]
    return ids

def extract_answer_text(response: str):
    """
    Restituisce solo il testo della risposta, togliendo 'FILE_UTILIZZATI[...]:' iniziale.
    """
    match = re.match(r'FILE_UTILIZZATI\[[^\]]*\]:\s*(.*)', response, re.DOTALL)
    if match:
        return match.group(1).strip()
    return response.strip()