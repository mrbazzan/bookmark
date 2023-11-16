
from commands import (
    CreateBookmarksTableCommand as initialize_db,
    ListBookmarksCommand as list_bookmarks,
    QuitCommand
)


def print_options(options):
    for short_key, option in options.items():
        print(f"({short_key}) {option} ")
    print()

def valid_option(choice, options):
    return choice in options or choice.upper() in options

def get_choice_from_input(options):
    choice = input("Choose an option: ")
    while not valid_option(choice, options):
        choice = input("Choose an option: ")
    return options[choice.upper()]

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

   options = {
        'B': Option("List bookmarks by date", list_bookmarks()),
        'Q': Option("Quit", QuitCommand())
    }

   print_options(options)

   choice = get_choice_from_input(options)
   choice.run()
