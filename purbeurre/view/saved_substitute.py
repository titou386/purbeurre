"""Saved substitution pages."""
import os
import platform
from purbeurre.constants import \
    HOMEPAGE,                   \
    SAVED_SUBSITITUTE,          \
    DETAILED_SUBSTITUTE,        \
    EXIT


class SavedSubstituteView:
    """Saved substitution class."""

    def display(self, results=None):
        """Display the page."""
        os.system("cls" if platform.system() == "Windows" else "clear")
        print("""
# Page des subtituts sauvegardés
""")
        if not results:
            print("Aucun substitut sauvegardé pour l'instant.\n")
            return

        for i in range(len(results)):
            print("{}- {}  -->  {}".format(i, results[i][1],
                  results[i][3]))
        print()

    def get_next_page(self, max):
        """Determine the next page."""
        while True:
            print("h - Page d'accueil   q - Quitter")
            if max > 0:
                print("s - Supprimer un substitut")
                print("d - Detail d'un substitut")
            option = input("option? ")
            if option == 'h':
                return (HOMEPAGE, None)
            elif option == 's' or option == 'd' and max > 0:
                index = input("Numéro? ")
                try:
                    index = int(index)
                    if index >= 0 or index < max:
                        if option == 's':
                            return (SAVED_SUBSITITUTE, index)
                        else:
                            return (DETAILED_SUBSTITUTE, index)
                except (ValueError, TypeError):
                    pass

            elif option == 'q':
                return (EXIT, None)
            else:
                return (SAVED_SUBSITITUTE, None)
