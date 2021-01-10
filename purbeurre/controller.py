"""Page management."""
from purbeurre.db.manager import Manager

from purbeurre.view.homepage import HomePageView
from purbeurre.view.product_search import ProductSearchView
from purbeurre.view.category_search import CategorySearchView
from purbeurre.view.product_search_result import ProductSearchResultView
from purbeurre.view.category_search_result import CategorySearchResultView
from purbeurre.view.product_detail import ProductDetailView
from purbeurre.view.saved_substitute import SavedSubstituteView
from purbeurre.view.exit import ExitView


from purbeurre.constants import \
    PRODUCT_SEARCH,             \
    CATEGORY_SEARCH,            \
    HOMEPAGE,                   \
    PRODUCT_SEARCH_RESULT,      \
    CATEGORY_SEARCH_RESULT,     \
    PRODUCT_DETAIL,             \
    SAVED_SUBSITITUTE,          \
    DETAILED_SUBSTITUTE,        \
    PREVIOUS_PAGE,              \
    SAVE,                       \
    EXIT


class Controller:
    """Page management class."""

    def __init__(self):
        """Controller contructor."""
        self.page = HOMEPAGE
        self.running = True
        self.search_type = None
        self.category_id = None
        self.product_id = None
        self.substitute_id = None
        self.input = None

        self.manager = Manager()

    def run(self):
        """Page management."""
        while self.running:
            if self.page == HOMEPAGE:
                view = HomePageView()
                view.display()
                self.page = view.get_next_page()

            elif self.page == PRODUCT_SEARCH:
                self.search_type = self.page
                self.category_id = None
                self.product_id = None
                self.substitute_id = None
                view = ProductSearchView()
                view.display()
                self.page, self.input = view.get_next_page()

            elif self.page == CATEGORY_SEARCH:
                self.search_type = self.page
                self.category_id = None
                self.product_id = None
                self.substitute_id = None
                view = CategorySearchView()
                view.display()
                self.page, self.input = view.get_next_page()

            elif self.page == CATEGORY_SEARCH_RESULT:
                self.category_id = None
                self.product_id = None
                self.substitute_id = None
                results = self.manager.search_category_name(self.input)
                view = CategorySearchResultView()
                view.display([r[1] for r in results])
                self.page, option = view.get_next_page(len(results))
                if option or option == 0:
                    self.category_id = results[option][0]

            elif self.page == PRODUCT_SEARCH_RESULT:
                self.product_id = None
                self.substitute_id = None
                if self.category_id:
                    results = self.manager.\
                        product_in_category(self.category_id)
                else:
                    results = self.manager.search_product_name(self.input)
                view = ProductSearchResultView()
                view.display([r[1] for r in results])
                self.page, option = view.get_next_page(len(results))
                if option or option == 0:
                    self.product_id = results[option][0]

            elif self.page == PRODUCT_DETAIL:
                saved = False
                save_function = True
                prod_dtl = self.manager.product_detail(self.product_id)
                if not self.substitute_id:
                    self.substitute_id = self.manager.\
                        get_product_subtitution(self.product_id)
                if self.manager.db.get("substitution",
                                       {'product_id': self.product_id}):
                    saved = True
                    save_function = False
                if self.substitute_id:
                    sub_dtl = self.manager.product_detail(self.substitute_id)
                else:
                    sub_dtl = None
                view = ProductDetailView()
                view.display(prod_dtl, sub_dtl, saved)
                self.page, option = view.get_next_page(save_function)
                if option == SAVE:
                    self.manager.save_substitute(
                        self.product_id, self.substitute_id)

            elif self.page == SAVED_SUBSITITUTE:
                self.input = None
                results = self.manager.substitution_saved()
                view = SavedSubstituteView()
                view.display(results)
                self.page, value = view.get_next_page(len(results))
                if value or value == 0 and self.page == SAVED_SUBSITITUTE:
                    self.manager.delete_substitute(results[value][0])
                elif value or value == 0 and self.page == DETAILED_SUBSTITUTE:
                    self.product_id = results[value][0]
                    self.substitute_id = results[value][2]

            elif self.page == DETAILED_SUBSTITUTE:
                self.input = None
                product = self.manager.product_detail(self.product_id)
                substitute = self.manager.product_detail(self.substitute_id)
                view = ProductDetailView()
                view.display(product, substitute)
                self.page, value = view.get_next_page()

            elif self.page == EXIT:
                self.running = False
                view = ExitView()
                view.display()

            elif self.page == PREVIOUS_PAGE:
                if self.substitute_id and not self.input:
                    self.page = HOMEPAGE
                elif self.product_id:
                    self.page = PRODUCT_SEARCH_RESULT
                elif self.category_id:
                    self.page = CATEGORY_SEARCH_RESULT
                else:
                    self.page = HOMEPAGE
