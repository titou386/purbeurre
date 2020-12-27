import os

from purbeurre.constants import \
    HOMEPAGE,                   \
    PRODUCT_SEARCH_RESULT,      \
    EXIT


class ProductSearchView:

    def display(self):
        os.system('clear')
        print("""
# Page de recherche de produits

h! - Page d'acceuil
q! - Quitter

""")

    def get_next_page(self):
        option = input("Produit? ")
        if option == "h!":
            return (HOMEPAGE, None)
        elif option == "q!":
            return (EXIT, None)
        else:
            return (PRODUCT_SEARCH_RESULT, option)
