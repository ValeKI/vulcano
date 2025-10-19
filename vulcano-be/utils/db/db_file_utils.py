from db import get_cursor

def db_insert_file(file_name, format, user_id):
    cur = get_cursor()
    cur.execute(
        "INSERT INTO files (file_name, format, user_id) VALUES (%s, %s, %s) RETURNING file_id",
        (file_name, format, user_id)
    )
    # Effettua il commit esplicito
    if hasattr(cur, "connection"):
        cur.connection.commit()
    result = cur.fetchone()
    print(f"Inserted file with ID: {result} (type: {type(result)})")
    if not result:
        return None
    if isinstance(result, dict):
        return result.get('file_id')
    # Se è una tupla, prendi il primo elemento
    return result[0]

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
        "SELECT COUNT(*) AS count FROM files WHERE file_name LIKE %s AND user_id=%s",
        (like_pattern, user_id)
    )
    result = cur.fetchone()
    # Gestione sia per tuple che per dict
    if not result:
        return 0
    if isinstance(result, dict):
        return result.get('count', 0)
    return result[0]

def list_files_for_user(user_id):
    cur = get_cursor()
    cur.execute(
        "SELECT file_name, format FROM files WHERE user_id=%s",
        (user_id,)
    )
    return cur.fetchall()

def get_file_by_id(file_id):
    cur = get_cursor()
    cur.execute(
        "SELECT file_id, file_name, user_id, format FROM files WHERE file_id=%s",
        (file_id,)
    )
    result = cur.fetchone()
    return result
