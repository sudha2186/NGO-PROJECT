import sqlite3

class Database:
    def __init__(self, database_path):
        self.database_path = database_path
        
    def execute(self, query, params=(), fetch_one=False, fetch_all=False):
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            print("Executing query:", query)
            print("With parameters:", params)
            cursor.execute(query, params)
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            else:
                result = None
            conn.commit()
        finally:
            conn.close()

        return result