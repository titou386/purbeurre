"""Product search class page."""
import os
import platform
from purbeurre.view.common import GenericFormatting
from purbeurre.constants import \
    HOMEPAGE,                   \
    PRODUCT_DETAIL,             \
    PREVIOUS_PAGE,              \
    EXIT


class ProductSearchResultView(GenericFormatting):
    """Product search result class."""

    def display(self, results):
        """Display the page."""
        os.system("cls" if platform.system() == "Windows" else "clear")
        print("# Page de résultat des produits :\n")
        self.format_results(results)

    def get_next_page(self, max):
        """Determine the next page."""
        while True:
            print("\nh - Page d'accueil   r - retour   q - Quitter")
            option = input("Choix? ")
            if option == 'h':
                return (HOMEPAGE, None)
            elif option == 'r':
                return (PREVIOUS_PAGE, None)
            elif option == 'q':
                return (EXIT, None)
            else:
                try:
                    option = int(option)
                    if option >= 0 and option < max:
                        return (PRODUCT_DETAIL, option)
                except ValueError:
                    pass
