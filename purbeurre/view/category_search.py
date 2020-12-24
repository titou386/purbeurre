import os
from purbeurre.constants import \
    HOMEPAGE,                   \
    CATEGORY_SEARCH_RESULT,     \
    EXIT


class SearchCategoryView:

    def display(self):
        os.system('clear')
        print("""
# Page de recherche de categories

h! - Page d'acceuil
q! - Quitter

""")

    def get_next_page(self):
        option = input("Produit? ")
        if option == "h!" or option == "H!":
            return (HOMEPAGE, None)
        elif option == "q!" or option == "Q!":
            return EXIT
        else:
            return (CATEGORY_SEARCH_RESULT, option)
