import requests
import json


class OpenFactFood:


    def __init__(self, nb_cat, nb_prod):

        self.nb_cat = nb_cat
        self.top_cat = []
        self.nb_prod = nb_prod
        self.products = []
        self.err = None
        self.get_top_categories()
        self.get_products()

    def log(self, msg):
        print(msg)

    def get_top_categories(self):
        self.top_cat = [None for e in range(self.nb_cat)]

        r = requests.get('https://fr.openfoodfacts.org/categories.json')
        if not r.ok:
            self.log('Une erreur s\'est produite lors de la récupération des catégories')
            self.log('Code erreur HTTP : ' + r.status_code)
            self.err = r.status_code
            return

        data = json.loads(r.text)
        for category in data['tags']:
            for i in range(len(self.top_cat)):
                if self.top_cat[i] is None or \
                   self.top_cat[i]["products"] < category["products"]:

                    self.top_cat.insert(i, category)
                    self.top_cat.pop(len(self.top_cat) - 1)
                    break


    def get_products(self):
        if self.err is not None:
            return

        for j in range(len(self.top_cat)):
            payload = {
                'action': 'process',
                'tagtype_0': 'categories',
                'tag_contains_0': 'contains',
                'tag_0': self.top_cat[j]['id'],
                'tagtype_1': 'countries',
                'tag_contains_1': 'contains',
                'tag_1': 'France',
                'page_size': self.nb_prod,
                'json': 'true'
            }

            r = requests.get('https://world.openfoodfacts.org/cgi/search.pl', params=payload)
            if not r.ok:
                self.log('Une erreur s\'est produite lors de la récupération des produits')
                self.log('Code erreur HTTP : ' + r.status_code)
                self.err = r.status_code
                return

            self.products.append(json.loads(r.text)['products'])



