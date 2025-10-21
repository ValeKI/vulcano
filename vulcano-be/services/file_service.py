from flask import Request, jsonify
from io import BytesIO
from dtos.common_dtos import ErrorResponseDTO
from dtos.file_dtos import UploadFileResponseDTO, DownloadFileResponseDTO, ListFilesResponseDTO, ListFilesByAnswerIdResponseDTO
from utils.file_utils import FileUtils
from utils.minio_utils import MinioUtils
from utils.auth_utils import AuthUtils
from utils.db.db_file_utils import DbFileUtils
from utils.qdrant_utils import QdrantUtils

class FileService:
    """
    Service per la gestione dei file utente: upload, download, lista e ricerca per answer.
    """

    def __init__(self, request: Request):
        """
        Inizializza il service con la richiesta Flask.
        Args:
            request (Request): Oggetto request Flask.
        """
        self.request = request

    def upload_file(self):
        print("[SERVICE] upload_file called")
        """
        Gestisce l'upload di un file per l'utente corrente.
        Returns:
            dict: Risultato.
            DTO: UploadFileResponseDTO, ErrorResponseDTO
        """
        if "file" not in self.request.files:
            return ErrorResponseDTO(error="Nessun file inviato")
        file = self.request.files["file"]
        if file.filename == "":
            return ErrorResponseDTO(error="Nome file mancante")
        auth_utils = AuthUtils(self.request)
        user_id = auth_utils.get_user_id_from_request()
        if user_id is None:
            return jsonify({"error": "Utente non autorizzato"}), 401
        file_utils = FileUtils()
        db_file_utils = DbFileUtils()
        new_file_name = file_utils.get_unique_file_name(file.filename, user_id)
        file_content = file.read()
        if not file_content:
            return ErrorResponseDTO(error="File vuoto")
        minio_utils = MinioUtils()
        minio_utils.upload_user_file(user_id, new_file_name, file_content)
        file_id = file_utils.insert_new_file(new_file_name, user_id)
        # oppure direttamente: file_id = db_file_utils.db_insert_file(new_file_name, format, user_id)
        qdrant_utils = QdrantUtils()
        num_chunks = qdrant_utils.upload_file_chunks_to_qdrant(user_id, file_id, new_file_name, file_content)
        if num_chunks == 0:
            return ErrorResponseDTO(error="File vuoto o non processabile")
        print("[SERVICE] upload_file completed")
        return UploadFileResponseDTO(status="ok", filename=new_file_name)

    def download_file(self):
        print("[SERVICE] download_file called")
        """
        Restituisce il file richiesto dall'utente.
        Returns:
            dict: File info.
            DTO: DownloadFileResponseDTO, ErrorResponseDTO
        """
        file_id = self.request.args.get("file_id")
        if not file_id:
            return ErrorResponseDTO(error="ID file mancante")
        auth_utils = AuthUtils(self.request)
        user_id = auth_utils.get_user_id_from_request()
        if user_id is None:
            return jsonify({"error": "Utente non autorizzato"}), 401
        db_file_utils = DbFileUtils()
        file_name = db_file_utils.get_file_by_id(file_id)["file_name"]
        minio_utils = MinioUtils()
        file_data = minio_utils.get_user_file(user_id, file_name)
        print("[SERVICE] download_file completed")
        return DownloadFileResponseDTO(file_data=file_data, file_name=file_name)

    def list_files(self):
        print("[SERVICE] list_files called")
        """
        Restituisce la lista dei file dell'utente corrente.
        Returns:
            dict: Lista file.
            DTO: ListFilesResponseDTO, ErrorResponseDTO
        """
        auth_utils = AuthUtils(self.request)
        user_id = auth_utils.get_user_id_from_request()
        if user_id is None:
            return jsonify({"error": "Utente non autorizzato"}), 401
        qdrant_utils = QdrantUtils()
        db_file_utils = DbFileUtils()
        file_ids = qdrant_utils.get_file_ids_by_user_id(user_id)
        files = []
        for file_id in file_ids:
            file_data = db_file_utils.get_file_by_id(file_id)
            if file_data:
                files.append(file_data)
        print("[SERVICE] list_files completed")
        return ListFilesResponseDTO(files=files)

    def list_files_by_answer_id(self):
        print("[SERVICE] list_files_by_answer_id called")
        """
        Restituisce la lista dei file associati a una risposta.
        Returns:
            dict: Lista file.
            DTO: ListFilesByAnswerIdResponseDTO, ErrorResponseDTO
        """
        answer_id = self.request.args.get("answer_id")
        if not answer_id:
            return ErrorResponseDTO(error="answer_id mancante")
        try:
            answer_id = int(answer_id)
        except Exception:
            return ErrorResponseDTO(error="answer_id non valido")
        qdrant_utils = QdrantUtils()
        db_file_utils = DbFileUtils()
        file_ids = qdrant_utils.get_file_ids_by_answer_id(answer_id)
        files = []
        for file_id in file_ids:
            file_data = db_file_utils.get_file_by_id(file_id)
            if file_data:
                files.append(file_data)
        print("[SERVICE] list_files_by_answer_id completed")
        return ListFilesByAnswerIdResponseDTO(files=files)
