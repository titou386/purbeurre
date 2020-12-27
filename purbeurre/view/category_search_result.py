import os
from purbeurre.view.common import GenericFormatting
from purbeurre.constants import \
    HOMEPAGE,               \
    PRODUCT_SEARCH_RESULT, \
    EXIT


class CategorySearchResultView(GenericFormatting):

    def __init__(self, results):
        self.results = results

    def display(self):
        os.system('clear')
        print("""
# Page de résultat des catégories :
""")
        self.format_results(self.results)

    def get_next_page(self):
        print()
        while True:
            print("""h - Page d'acceuil   r - retour   q - Quitter""")
            option = input("Choix? ")
            if option == "h" or option == "H":
                return (HOMEPAGE, None)
            elif option == 'r' or option == 'R':
                return ("previous_page", None)
            elif option == "q" or option == "Q":
                return (EXIT, None)
            else:
                try:
                    option = int(option)
                    if option >= 0 and option < len(self.results):
                        return (PRODUCT_SEARCH_RESULT, option)
                except ValueError:
                    pass
