import os
from purbeurre.constants import \
    HOMEPAGE,                   \
    PRODUCT_VIEW,               \
    EXIT


class ProductDetailView:

    def __init__(self, product, substitute):
        self.product = product
        self.substitute = substitute

    def display(self):
        os.system('clear')
        print("""
# Page de détail du produits :
    # Produit :
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
            return (PRODUCT_VIEW, option)
