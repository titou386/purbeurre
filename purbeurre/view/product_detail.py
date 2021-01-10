"""Product detail pages."""
import os
from purbeurre.constants import \
    HOMEPAGE,                   \
    PRODUCT_DETAIL,             \
    PREVIOUS_PAGE,              \
    SAVE,                       \
    EXIT


class ProductDetailView:
    """Product detail class."""

    def display(self, product, substitution, saved=False):
        """Display the page.

        Parameters:
            product(list): a list (int/str)
            substitution(list): a list (int/str)
            saved(bool): If True, display a message
        """
        os.system('clear')
        print("# Page de détail du produit :")
        prod_card(product)

        if substitution:
            print("# Produit de substitution")
            prod_card(substitution)
        else:
            print("Aucun produit de substitution n'a été trouvé.")

        if saved:
            print("Ce produit est dans vos substituts.")

    def get_next_page(self, save_function=False):
        """Determine the next page."""
        while True:
            print("\nh - Page d'accueil   r - retour   q - Quitter")
            if save_function:
                print("s - Saugarder le produit de substitution")

            option = input("Choix? ")
            if option == "h":
                return (HOMEPAGE, None)
            elif option == 'r':
                return (PREVIOUS_PAGE, None)
            elif option == "q":
                return (EXIT, None)
            elif option == 's' and save_function:
                return (PRODUCT_DETAIL, SAVE)


def prod_card(prod):
    """Product sheet."""
    prod = [p if p is not None else '' for p in prod]

    print("""
Nom du produit :   {}
Description :      {}
Quantité :         {}
Magasin de vente : {}
Pays de vente :    {}

Pour 100g/ml
Energie :          {}{}
Matières grasses : {}{}
   dont saturées : {}{}
Glucides :         {}{}
     dont sucres : {}{}
Fibres :           {}{}
Protéines :        {}{}
Sel :              {}{}

Nutriscore :       {}
Nova :             {}
URL de la fiche :  https://fr.openfoodfacts.org/produit/{}
\n""".format(prod[1], prod[2], prod[3], prod[4], prod[5],
             prod[6], prod[7],
             prod[8], prod[9],
             prod[10], prod[11],
             prod[12], prod[13],
             prod[14], prod[15],
             prod[16], prod[17],
             prod[18], prod[19],
             prod[20], prod[21],
             prod[22],
             prod[23],
             prod[24]
             ))
