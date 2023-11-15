
import sys

from database import DatabaseManager
from datetime import datetime

db = DatabaseManager("bookmark.db")

class QuitCommand:
    def execute(self):
        sys.exit()

class CreateBookmarksTableCommand:
    def execute(self):
        db.create_table(
            'bookmarks',
            {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "title": "TEXT NOT NULL",
                "url": "TEXT NOT NULL",
                "notes": "TEXT",
                "date_added": "TEXT NOT NULL"
            }
        )

class AddBookmarkCommand:
    def execute(self, data):
        data["date_added"] = datetime.utcnow().isoformat()
        db.add_record('bookmarks', data)
        return f"Bookmark '{data.get('title')}' added!"

class ListBookmarksCommand:
    def __init__(self, order_by="date_added"):
        self.order_by = order_by

    def execute(self):
        output = db.select_records(
            'bookmarks', order_by=self.order_by
        )
        return output.fetchall()

class DeleteBookmarkCommand:
    def execute(self, data):
        db.remove_record(
            'bookmarks', {"id": data}
        )
        return f"Bookmark deleted!"
