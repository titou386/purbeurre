"""api.py."""
import requests
import json
import logging
from purbeurre.constants import MAX_CATEGORIES, MAX_PRODUCTS


class OpenFoodFacts:
    """Retrieves data from the Open Food Facts API."""

    def __init__(self):
        """Open Food Facts' contructor require 2 arguments."""
        self.categories = []
        self.get_categories()

    def get_categories(self):
        """Method get_categories.

        Retrieve from the API and fill 'categories' variable with
        a decreasing ordered list.
        Returns:
            Nothing (fill up self.categories)
        """
        self.categories = [None for e in range(MAX_CATEGORIES)]

        r = requester('https://fr.openfoodfacts.org/categories.json')

        for category in r['tags']:
            for i in range(len(self.categories)):
                if self.categories[i] is None or \
                   self.categories[i]["products"] < category["products"]:

                    self.categories.insert(i, category)
                    self.categories.pop(len(self.categories) - 1)
                    break

    def get_products(self):
        """Method get_products.

        Retrieve from the API and fill 'products' variable with a list.
        Returns:
            Dict value if it succeeded
            None if it failed
        """
        try:
            cat = self.categories.pop(0)
            payload = {
                'action': 'process',
                'tagtype_0': 'categories',
                'tag_contains_0': 'contains',
                'tag_0': cat['id'],
                'tagtype_1': 'countries',
                'tag_contains_1': 'contains',
                'tag_1': 'France',
                'page_size': MAX_PRODUCTS,
                'json': 'true'
            }

            r = requester('https://world.openfoodfacts.org/cgi/search.pl',
                          params=payload)

            return r['products']
        except(IndexError, TypeError) as e:
            logging.error('api.py:get_products():{}'.format(e))
            return None


def requester(url, **kwargs):
    """Similar to requests.get.

    Parameters:
        url(str): url with http://

        parameter named:
            params(key)(str) take same paramaters than requests

    Returns:
        dict: json converted
        None if it failed
    """
    if ('params' in kwargs):
        r = requests.get(url, kwargs['params'])
    else:
        r = requests.get(url)

    if r.ok:
        return json.loads(r.text)
    else:
        logging.error('api.py:requester():Une erreur s\'est produite \
lors de la récupération des données')
        logging.error('api.py:requester():Code erreur HTTP : {}'.
                      format(r.status_code))
        return None
