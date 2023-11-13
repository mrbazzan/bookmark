
import sqlite3

class DatabaseManager:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)

    def _execute(self, stmt, values=None):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(stmt, values or [])
            return cursor

    def create_table(self, table_name, columns):
        col_with_types = [
            col + ' ' + constraints
            for col, constraints in columns.items()
        ]
        self._execute(
            f"""
                CREATE TABLE IF NOT EXISTS {table_name}(
                {", ".join(col_with_types)});
            """
        )

    def __del__(self):
        self.conn.close()
