
import os

from commands import (
    CreateBookmarksTableCommand as initialize_db,
    AddBookmarkCommand as add_bookmark,
    ListBookmarksCommand as list_bookmarks,
    DeleteBookmarkCommand as delete_bookmark,
    GithubStarImportCommand as stars_import,
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

def get_label(label, required=True):
    prompt = input(label)
    while required and (not prompt):
        prompt = input(label)
    return prompt

def add():
    data = dict()
    data["title"] = get_label("Title: ")
    data["url"] = get_label("Url: ")
    data["notes"] = get_label("Notes: ", required=False)
    return data

def delete():
    return get_label("Id: ")

def github_stars_prompt():
    return {
        "github_username": get_label("Github username: "),
        "preserve": get_label(
            "Preserve timestamps [Y/n]: ",
            required=False
        ) in {'Y', 'y', ''}
    }

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

class Option:
    def __init__(self, option, command, extra=None):
        self.option = option
        self.command = command
        self.extra = extra

    def run(self):
        prep = self.extra() if self.extra else None
        output = self.command.execute(prep)
        print(output)

    def __str__(self):
        return self.option

def main():
   options = {
        'A': Option("Add a bookamrk", add_bookmark(), extra=add),
        'B': Option("List bookmarks by date", list_bookmarks()),
        'T': Option("List bookamrks by title", list_bookmarks(order_by="title")),
        'D': Option("Delete a bookmark", delete_bookmark(), extra=delete),
        'G': Option("Import GitHub stars", stars_import(), extra=github_stars_prompt),
        'Q': Option("Quit", QuitCommand())
    }

   clear_screen()
   print_options(options)

   choice = get_choice_from_input(options)
   clear_screen()
   choice.run()

   input("Press ENTER to return to options")

if __name__ == "__main__":
   initialize_db().execute()

   while True:
       main()
