import os
from utils.db.db_file_utils import DbFileUtils

class FileUtils:
    def get_unique_file_name(self, file_name, user_id):
        db_file_utils = DbFileUtils()
        name, ext = os.path.splitext(file_name)
        if db_file_utils.file_exists_for_user(file_name, user_id):
            count = db_file_utils.count_files_with_base_name(name, ext, user_id)
            return f"{name}_{count}{ext}"
        return file_name

    def insert_new_file(self, file_name, user_id):
        db_file_utils = DbFileUtils()
        format = os.path.splitext(file_name)[1].lstrip('.')
        file_id = db_file_utils.db_insert_file(file_name, format, user_id)
        return file_id
