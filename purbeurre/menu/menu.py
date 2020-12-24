import os


class Menu:
    """Menu for purbeurre application."""

    def __init__(self):
        self.term_columns = 0
        self.term_lines = 0

    def get_terminal_size(self):
        self.term_columns = os.get_terminal_size().columns
        self.term_colulns = os.get_terminal_size().lines


    def print_menu(self, message):
        os.system('clear')
        self.get_size()

        print(message)
        return input()

    



class SearchByCaetago