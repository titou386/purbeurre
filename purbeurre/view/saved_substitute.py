import os
from purbeurre.constants import \
    HOMEPAGE,                   \
    SAVED_SUBSITITUTE,        \
    EXIT



class SavedSubstituteView:
    def __init__(self, results):
        self.results = results

    def display(self):
        os.system('clear')
        print("""
# Page des substitus sauvegardés
""")
        if not self.results:
            print("Aucun substitu sauvegardé pour l'instant.\n")
            return

        for i in range(len(self.results)):
            print("{}- {}  -->  {}".format(i, self.results[i][1], self.results[i][3]))
        print()


    def get_next_page(self):
        print("h - Page d'acceuil q - Quitter")
        if self.results:
            print("s - pour supprimer un substitut")
        option = input("option? ")
        if option == "h":
            return (HOMEPAGE, None)
        elif option == "s" and self.results:
            index = input("Numéro ? ")
            try:
                index = int(index)
                if index >= 0 or index < len(self.results):
                    return (SAVED_SUBSITITUTE, index)
            except ValueError:
                pass
        elif option == "q":
            return (EXIT, None)
        else:
            return (SAVED_SUBSITITUTE, None)
