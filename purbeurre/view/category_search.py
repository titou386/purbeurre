"""Category search page."""
import os
import platform
from purbeurre.constants import \
    HOMEPAGE,                   \
    CATEGORY_SEARCH_RESULT,     \
    EXIT


class CategorySearchView:
    """Category search class."""

    def display(self):
        """Display the page."""
        os.system("cls" if platform.system() == "Windows" else "clear")
        print("""
# Page de recherche de catégories

h! - Page d'accueil
q! - Quitter

""")

    def get_next_page(self):
        """Determine the next page."""
        option = input("Catégorie? ")
        if option == "h!":
            return (HOMEPAGE, None)
        elif option == "q!":
            return (EXIT, None)
        else:
            return (CATEGORY_SEARCH_RESULT, option)
