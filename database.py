
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

    def add_record(self, table_name, columns):
        self._execute(
            f"""
                INSERT INTO {table_name} (title, url, notes, date_added)
                VALUES ({', '.join('?' * len(columns))})
            """,
            tuple(columns.values())
        )

    def remove_record(self, table_name, columns):
        placeholders = [f"{column} = ?" for column in columns]
        self._execute(
            f"""
                DELETE FROM {table_name}
                WHERE {" AND ".join(placeholders)};
            """,
            tuple(columns.values())
        )

    def select_records(self, table_name, columns={}, order_by=None):
        query = f"SELECT * FROM {table_name}"

        if columns:
            placeholders = [f"{column} = ?" for column in columns]
            select_stmt = " AND ".join(placeholders)
            query += f" WHERE {select_stmt}"

        if order_by:
            query += f" ORDER BY {order_by}"

        query += ";"
        return self._execute(query, tuple(columns.values()))

    def __del__(self):
        self.conn.close()
