import pyodbc
from config import CONNECTION_STRING

def get_db_connection():
    return pyodbc.connect(CONNECTION_STRING)

def execute_query(query, params=None, fetch=False):
    conn = get_db_connection()
    cursor = conn.cursor()
   

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    if fetch:
        rows = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return rows

    conn.commit()
    cursor.close()
    conn.close()
    return None