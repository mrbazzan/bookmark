
from database import DatabaseManager
from abc import ABC, abstractmethod

class PersistenceLayer(ABC):
    @abstractmethod
    def add(self):
        raise NotImplementedError("There must be a 'create' method")

    @abstractmethod
    def read(self):
        raise NotImplementedError("There must be a 'read' method")

    @abstractmethod
    def delete(self):
        raise NotImplementedError("There must be a 'delete' method")

class BookmarkDatabase(PersistenceLayer):
    def __init__(self):
        self._table_name = "bookmarks"
        self._db = DatabaseManager("bookmark.db")
        self._db.create_table(self._table_name, {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "title": "TEXT NOT NULL",
            "url": "TEXT NOT NULL",
            "notes": "TEXT",
            "date_added": "TEXT NOT NULL"
        })

    def add(self, bookmark_data):
        self._db.add_record(self._table_name, bookmark_data)

    def read(self, order_by=None):
        return self._db.select_records(
            self._table_name, order_by=order_by).fetchall()

    def delete(self, bookmark_id):
        self._db.remove_record(self._table_name, {"id": bookmark_id})


