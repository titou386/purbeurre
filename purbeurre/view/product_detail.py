import os
from purbeurre.constants import \
    HOMEPAGE,                   \
    PRODUCT_DETAIL,               \
    EXIT


class ProductDetailView:

    def __init__(self, product, substitute):
        self.product = product
        self.substitute = substitute

    def display(self):
        os.system('clear')
        print("""
# Page de détail du produit :""")
        prod_card(self.product)

        if self.substitute:
            print("""
# Produit de substitution""")
            prod_card(self.substitute)

    def get_next_page(self):
        while True:
            print()
            print("""h - Page d'acceuil   r - retour   q - Quitter""")
            if self.substitute:
                print("s - Saugarder le produit de substitution")

            option = input("Choix? ")
            if option == "h":
                return (HOMEPAGE, None)
            elif option == 'r':
                return ("previous_page", None)
            elif option == "q":
                return (EXIT, None)
            elif option == 's' and self.substitute:
                return (PRODUCT_DETAIL, "save")


def prod_card(prod):
    prod = [p if p else 'NC' for p in prod]

    print("""
Nom du produit :   {}
Description :      {}
Magasin de vente : {}
Pays de vente :    {}

Pour 100g
Matières grasses : {}
   dont saturées : {}
Glucides :         {}
Sel :              {}

Nutriscore :       {}
Nova :             {}
URL de la fiche :  https://fr.openfoodfacts.org/produit/{}\
""".format(prod[2], prod[3], prod[4], prod[5],
           prod[9], prod[10], prod[11], prod[12],
           prod[8], prod[7], prod[1]))

