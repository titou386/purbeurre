"""Product search page."""
import os

from purbeurre.constants import \
    HOMEPAGE,                   \
    PRODUCT_SEARCH_RESULT,      \
    EXIT


class ProductSearchView:
    """Product search class."""

    def display(self):
        """Display the page."""
        os.system('clear')
        print("""
# Page de recherche de produits

h! - Page d'accueil
q! - Quitter

""")

    def get_next_page(self):
        """Determine the next page."""
        option = input("Produit? ")
        if option == "h!":
            return (HOMEPAGE, None)
        elif option == "q!":
            return (EXIT, None)
        else:
            return (PRODUCT_SEARCH_RESULT, option)
