
from commands import (
    CreateBookmarksTableCommand as initialize_db,
)


class Option:
    def __init__(self, option, command, extra=None):
        self.option = option
        self.command = command
        self.extra = extra

    def run(self):
        prep = self.extra() if self.extra else None
        output = self.command.execute(prep) if prep else self.command.execute()
        print(output)

    def __str__(self):
        return self.option

if __name__ == "__main__":
   initialize_db().execute()
   print("Welcome")
