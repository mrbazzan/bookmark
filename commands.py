
import sys
import requests

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
    def execute(self, data, timestamp=None):
        data["date_added"] = timestamp or datetime.utcnow().isoformat()
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

class GithubStarImportCommand:
    @staticmethod
    def _get_next_link(links):
        for link in links:
            if link.endswith("rel=\"next\""):
                return link.split(";")[0].strip()[1:-1]
        return

    @staticmethod
    def _process_url(url):
        r = requests.get(url, headers={"Accept": "application/vnd.github.v3.star+json"})
        links = r.headers.get("Link", "").split(",")
        return GithubStarImportCommand._get_next_link(links), r.json()

    def execute(self, data):
        github_username  = data.get("github_username")
        preserve_timestamps = data.get("preserve")
        imported_bookmark = 0

        url = f"https://api.github.com/users/{github_username}/starred"
        while url:
            url, response = GithubStarImportCommand._process_url(url)
            for repo_info in response:
                repo = repo_info.get("repo")
                bookmark = {
                    "title": repo.get("full_name"),
                    "url": repo.get("html_url"),
                    "notes": repo.get("description"),
                }
                imported_bookmark += 1

                timestamp = None
                if preserve_timestamps:
                    timestamp = repo_info.get("starred_at")

                AddBookmarkCommand().execute(bookmark, timestamp)

        return f"Imported {imported_bookmark} bookmarks from starred repos!"
