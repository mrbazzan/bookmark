
import sys
import requests

from abc import ABC, abstractmethod
from persistence import BookmarkDatabase
from datetime import datetime

bookmark_db = BookmarkDatabase()

class Command(ABC):
    def execute(self, data):
        raise NotImplementedError

class QuitCommand(Command):
    def execute(self, data=None):
        sys.exit()

class AddBookmarkCommand(Command):
    def execute(self, data, timestamp=None):
        data["date_added"] = timestamp or datetime.utcnow().isoformat()
        bookmark_db.add(data)
        return (True, data.get("title"))

class ListBookmarksCommand(Command):
    def __init__(self, order_by="date_added"):
        self.order_by = order_by

    def execute(self, data=None):
        return True, bookmark_db.read(order_by=self.order_by)

class DeleteBookmarkCommand(Command):
    def execute(self, data):
        bookmark_db.delete(data)
        return (True, data)

class GithubStarImportCommand(Command):
    def execute(self, data):
        github_username  = data.get("github_username")
        preserve_timestamps = data.get("preserve")
        imported_bookmark = 0

        url = f"https://api.github.com/users/{github_username}/starred"
        while url:
            response = requests.get(url, headers={"Accept": "application/vnd.github.v3.star+json"})
            url = response.links.get('next', {}).get('url', None)
            for repo_info in response.json():
                repo = repo_info.get("repo")
                bookmark = {
                    "title": repo.get("full_name"),
                    "url": repo.get("html_url"),
                    "notes": repo.get("description"),
                }
                imported_bookmark += 1

                timestamp = None
                if preserve_timestamps:
                    timestamp = datetime.strptime(
                        repo_info.get("starred_at"),
                        '%Y-%m-%dT%H:%M:%SZ'
                    )
                AddBookmarkCommand().execute(bookmark, timestamp)

        return (True, imported_bookmark)
