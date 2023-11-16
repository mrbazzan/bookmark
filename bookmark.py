
from commands import (
    CreateBookmarksTableCommand as initialize_db,
)


if __name__ == "__main__":
   initialize_db().execute()
   print("Welcome")
