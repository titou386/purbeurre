# -*- coding: utf-8 -*-
"""api.py."""
import requests
import json
import logging


class OpenFoodFacts:
    """Retrieves data from the Open Food Facts API."""

    def __init__(self, nb_cat, nb_prod):
        """Open Food Facts' contructor require 2 arguments.

        :param int nb_cat:
            Defined how many categories should be retrieved

        :param int nb_prod:
            Defined how many products in each category should be retrieved
        """
        self.nb_cat = nb_cat
        self.categories = []
        self.nb_prod = nb_prod
        self.products = []
        self.get_categories()

    def get_categories(self):
        """Method get_categories.

        Retrieve from the API and fill 'categories' variable with
        a decreasing ordered list.
        """
        self.categories = [None for e in range(self.nb_cat)]

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
        """
        for cat in self.categories:
            payload = {
                'action': 'process',
                'tagtype_0': 'categories',
                'tag_contains_0': 'contains',
                'tag_0': cat['id'],
                'tagtype_1': 'countries',
                'tag_contains_1': 'contains',
                'tag_1': 'France',
                'page_size': self.nb_prod,
                'json': 'true'
            }

            r = requester('https://world.openfoodfacts.org/cgi/search.pl',
                          params=payload)

            self.products.append([prod for cat in r['products']
                                  for prod in cat])


def requester(url, **kwargs):
    """Similar to requests.get."""
    if ('params' in kwargs):
        r = requests.get(url, kwargs['params'])
    else:
        r = requests.get(url)

    if r.ok:
        return json.loads(r.text)
    else:
        logging.error('Une erreur s\'est produite \
                      lors de la récupération des données')
        logging.error('Code erreur HTTP : ' + r.status_code)
        return None
