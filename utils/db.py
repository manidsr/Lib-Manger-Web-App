import mysql.connector
from config import Config

def get_db():
    return mysql.connector.connect(**Config.DB_CONFIG)

def execute_query(query, params=None):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    
    if query.strip().upper().startswith('SELECT'):
        result = cursor.fetchall()
    else:
        conn.commit()
        result = None
        
    cursor.close()
    conn.close()
    return result