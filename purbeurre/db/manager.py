import purbeurre.db.database


class Manager:
    """Class manager."""

    def __init__(self):
        """Create an mysql instance."""
        self.db = purbeurre.db.database.Mysql()

    def setup(self):
        """Database initialisation."""
        self.db.apply_structure()

    def insert_product(self, product_dict):
        """Insert one product in database."""
        values = {}
        for key in ('code', 'product_name', 'generic_name',
                    'stores', 'countries'):
            try:
                # Somes tags are missing or empty and can be replaced
                if key == 'product_name' or key == 'generic_name':
                    if key not in product_dict:
                        values[key] = product_dict[key + '_fr']
                    elif product_dict[key] == '':
                        values[key] = product_dict[key + '_fr']
                    else:
                        values[key] = product_dict[key]
                else:
                    values[key] = product_dict[key]
            except KeyError:
                pass

        product_id = self.db.insert("product", values)
        if not product_id:
            return
        self.insert_nutriments(product_id, product_dict)

        """Some tags are wrongly formatted"""
        if "categories_old" in product_dict:
            product_dict['categories'] = product_dict['categories_old']
        try:
            product_dict['categories'] = product_dict['categories']
            categories_list = product_dict['categories'].split(', ')
            if len(categories_list) == 1:
                categories_list = product_dict['categories'].split(',')
            for cat in categories_list:
                if has_coluns(cat):
                    categories_list[categories_list.index(cat)] = cat[3:]
        except KeyError:
            return

        for category_name in categories_list:
            category_id = self.insert_category(category_name)
            if not category_id:
                continue
            self.insert_product_category(product_id, category_id)

    def insert_product_category(self, product_id, category_id):
        """Insert one association (product, category) in database."""
        self.db.insert("product_category", {'product_id': product_id,
                                            'category_id': category_id})

    def insert_category(self, category_name):
        """Insert one category in database."""
        return self.db.insert("category", {'name': category_name})

    def insert_nutriments(self, product_id, product_dict):
        values = {}
        for key in ('nutriscore_grade', 'nutriments:fat_100g',
                    'nutriments:saturated-fat_100g', 'nutriments:sugars_100g',
                    'nutriments:salt_100g', 'nutriments:nova-group'):
            if has_coluns(key):
                try:
                    key1, key2 = key.split(':')
                    values[sql_formater(key2)] = product_dict[key1][key2]
                except KeyError:
                    pass
            else:
                try:
                    values[key] = product_dict[key]
                except KeyError:
                    pass
        values['product_id'] = product_id
        self.db.insert("nutriments", values)


def has_coluns(text):
    return False if text.find(':') == -1 else True


def sql_formater(text):
    return text.replace('-', '_')
