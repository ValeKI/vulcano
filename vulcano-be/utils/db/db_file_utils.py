from db import get_cursor

def insert_file(filename, format, user_id):
    cur = get_cursor()
    cur.execute(
        "INSERT INTO files (file_name, format, user_id) VALUES (%s, %s, %s)",
        (filename, format, user_id)
    )
    cur.connection.commit()

def file_exists_for_user(filename, user_id):
    cur = get_cursor()
    cur.execute(
        "SELECT 1 FROM files WHERE file_name=%s AND user_id=%s",
        (filename, user_id)
    )
    return cur.fetchone() is not None

def count_files_with_base_name(base_name, ext, user_id):
    cur = get_cursor()
    like_pattern = f"{base_name}%{ext}"
    cur.execute(
        "SELECT COUNT(*) FROM files WHERE file_name LIKE %s AND user_id=%s",
        (like_pattern, user_id)
    )
    result = cur.fetchone()
    return result[0] if result else 0

def list_files_for_user(user_id):
    cur = get_cursor()
    cur.execute(
        "SELECT file_name, format FROM files WHERE user_id=%s",
        (user_id,)
    )
    return cur.fetchall()
