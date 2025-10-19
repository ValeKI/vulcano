import os
from utils.db.db_file_utils import insert_file, file_exists_for_user, count_files_with_base_name

def get_unique_file_name(file_name, user_id):
    name, ext = os.path.splitext(file_name)
    if file_exists_for_user(file_name, user_id):
        count = count_files_with_base_name(name, ext, user_id)
        return f"{name}_{count}{ext}"
    return file_name

def insert_file_with_unique_name(file_name, user_id):
    format = os.path.splitext(file_name)[1].lstrip('.')
    insert_file(file_name, format, user_id)
    return file_name
