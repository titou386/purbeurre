"""Homepage."""
import os
from purbeurre.constants import \
    PRODUCT_SEARCH,             \
    CATEGORY_SEARCH,            \
    HOMEPAGE,                   \
    SAVED_SUBSITITUTE,        \
    EXIT


class HomePageView:
    """Home page class."""

    def display(self):
        """Display the page."""
        os.system('clear')
        print("""
# Page d'accueil

Bienvenue

Choisissez une option :

1 - Rechercher un produit par nom
2 - Rechercher une categorie
3 - Afficher mes substituts sauvegardés
q - Quitter

""")

    def get_next_page(self):
        """Determine the next page."""
        option = input("Choix? ")
        if option == "1":
            return PRODUCT_SEARCH
        elif option == "2":
            return CATEGORY_SEARCH
        elif option == "3":
            return SAVED_SUBSITITUTE
        elif option == "q" or option == "Q":
            return EXIT
        else:
            return HOMEPAGE
