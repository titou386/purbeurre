"""Constants for 'Purbeurre' application."""
import os

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

MAX_CATEGORIES = 15
MAX_PRODUCTS = 1000

HOMEPAGE = "homepage"

PRODUCT_SEARCH = "product_search"
CATEGORY_SEARCH = "category_search"

PRODUCT_SEARCH_RESULT = "product_search_result"
CATEGORY_SEARCH_RESULT = "category_search_result"

PRODUCT_DETAIL = "product_detail"

SAVED_SUBSITITUTE = "saved_substitute"
DETAILED_SUBSTITUTE = "detailed_substitute"

EXIT = "exit"

PREVIOUS_PAGE = "previous_page"
SAVE = "save"
