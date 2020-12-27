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
    EXIT


class Controller:

    def __init__(self):
        self.page = HOMEPAGE
        self.running = True
        self.search_type = None
        self.category_id = None
        self.product_id = None
        self.input = ""

        self.manager = Manager()

    def run(self):
        while self.running:
            if self.page == HOMEPAGE:
                view = HomePageView()
                view.display()
                self.page = view.get_next_page()

            elif self.page == PRODUCT_SEARCH:
                self.search_type = self.page
                self.category_id = None
                self.product_id = None
                view = ProductSearchView()
                view.display()
                self.page, self.input = view.get_next_page()

            elif self.page == CATEGORY_SEARCH:
                self.search_type = self.page
                self.category_id = None
                self.product_id = None
                view = CategorySearchView()
                view.display()
                self.page, self.input = view.get_next_page()

            elif self.page == CATEGORY_SEARCH_RESULT:
                self.category_id = None
                self.product_id = None
                results = self.manager.search_category_name(self.input)
                view = CategorySearchResultView([r[1] for r in results])
                view.display()
                self.page, option = view.get_next_page()
                if option or option == 0:
                    self.category_id = results[option][0]

            elif self.page == PRODUCT_SEARCH_RESULT:
                self.product_id = None
                if self.category_id:
                    results = self.manager.product_in_category(self.category_id)
                    view = ProductSearchResultView([r[1] for r in results])
                else:
                    results = self.manager.search_product_name(self.input)
                    view = ProductSearchResultView([r[2] for r in results])
                view.display()
                self.page, option = view.get_next_page()
                if option or option == 0:
                    self.product_id = results[option][0]

            elif self.page == PRODUCT_DETAIL:
                product = self.manager.product_id_detail(self.product_id)
                substitute = self.manager.get_substitute_product_id(self.product_id)
                view = ProductDetailView(product, substitute)
                view.display()
                self.page, option = view.get_next_page()
                if option == 'save':
                    self.manager.save_substitute(product[0], substitute[0])

            elif self.page == SAVED_SUBSITITUTE:
                results = self.manager.saved_substitute()
                view = SavedSubstituteView(results)
                view.display()
                self.page, value = view.get_next_page()
                if value or value == 0:
                    self.manager.delete_substitute_id(results[value][0])

            elif self.page == EXIT:
                self.running = False
                view = ExitView()
                view.display()

            elif self.page == "previous_page":
                if self.product_id:
                    self.page = PRODUCT_SEARCH_RESULT
                elif self.category_id:
                    self.page = CATEGORY_SEARCH_RESULT
                elif self.search_type:
                    self.page = self.search_type
                else:
                    self.page = HOMEPAGE
