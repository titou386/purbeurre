import os
from purbeurre.constants import \
    HOMEPAGE,               \
    PRODUCT_DETAIL, \
    EXIT


class ProductSearchResultView:

    def display(self, results):
        os.system('clear')
        print("""
# Page de résultat des produit :

""")

    def get_next_page(self, max):
        print("""h - Page d'acceuil   r - retour   q - Quitter""")
        option = input("Choix? ")
        if option == "h" or option == "H":
            return (HOMEPAGE, None)
        elif option == 'r' or option == 'R':
            return ("previous_page", None)
        elif option == "q" or option == "Q":
            return (EXIT, None)
        else:
            return (PRODUCT_DETAIL, option)
