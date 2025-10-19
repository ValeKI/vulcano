from db import get_cursor

def get_user_by_username_or_email(username_or_email):
    cur = get_cursor()
    cur.execute(
        "SELECT * FROM users WHERE username=%s OR email=%s",
        (username_or_email, username_or_email)
    )
    return cur.fetchone()

def get_user_by_email(email):
    cur = get_cursor()
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    return cur.fetchone()

def get_existing_user(email, username):
    cur = get_cursor()
    cur.execute("SELECT * FROM users WHERE email=%s OR username=%s", (email, username))
    return cur.fetchone()

def insert_user(username, email, hashed_pw):
    cur = get_cursor()
    cur.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (username, email, hashed_pw)
    )
    cur.connection.commit()

def update_user_password_and_reset_token(user_id, hashed_pw, token):
    cur = get_cursor()
    result = cur.execute(
        "UPDATE users SET password=%s, reset_token=NULL WHERE id=%s AND reset_token=%s",
        (hashed_pw, user_id, token)
    )
    cur.connection.commit()
    return cur.rowcount

def update_user_reset_token(user_id, reset_token):
    cur = get_cursor()
    cur.execute("UPDATE users SET reset_token=%s WHERE id=%s", (reset_token, user_id))
    cur.connection.commit()

def get_user_reset_token(user_id):
    cur = get_cursor()
    cur.execute("SELECT reset_token FROM users WHERE id=%s", (user_id,))
    return cur.fetchone()
