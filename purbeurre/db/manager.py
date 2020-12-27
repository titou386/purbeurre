import purbeurre.db.database
import logging


class Manager:
    """Class manager."""

    def __init__(self):
        """Create an mysql instance."""
        self.db = purbeurre.db.database.Mysql()

    def create_db(self):
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
        self.insert_nutriment(product_id, product_dict)

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

    def insert_nutriment(self, product_id, product_dict):
        """Insert one line in nutriments table."""
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
        self.db.insert("nutriment", values)

    def search_category_name(self, search):
        value = ["%{}%".format(search)]
        return self.db.query("category", value, where="name", like=True)

    def delete_substitute_id(self, product_id):
        self.db.delete('substitute',
                       {'product_id': product_id})

    def get_substitute_product_id(self, product_id):
        cat = [i[0] for i in self.db.query('product_category',
                                           (product_id,),
                                           select='category_id',
                                           where='product_id=%s')]

        prod = [p[0] for p in self.db.query('product_category', cat,
                                            select='product_id',
                                            where='category_id',
                                            inside='True')]

        while prod.count(product_id):
            prod.remove(product_id)

        occurence = [[] for c in cat]

        for p in prod:
            occurence[prod.count(p) - 1].append(p)
            while prod.count(p):
                prod.remove(p)

        index = len(occurence) - 1
        while not occurence[index]:
            index -= 1
        return self.db.query('product', tuple(occurence[index]),
                             join="nutriment",
                             on="product.id = nutriment.product_id",
                             where="nutriment.nutriscore_grade IS NOT NULL AND nutriment.product_id",
                             inside='True',
                             order_by='nutriscore_grade, nova_group',
                             limit=1)[0]

    def product_in_category(self, category_id):
        return self.db.query("product",
                             (category_id,),
                             select="product.id, product.product_name",
                             join="product_category",
                             on="product.id = product_category.product_id",
                             where="product_category.category_id=%s")

    def search_product_name(self, search):
        value = ["%{}%".format(search)]
        return self.db.query("product", value, where="product_name", like=True)

    def product_id_detail(self, product_id):
        return self.db.query("product",
                             (product_id,),
                             join="nutriment",
                             on="product.id = nutriment.product_id",
                             where="product.id=%s")[0]

    def save_substitute(self, product_id, substitute_id):
        self.db.insert('substitute',
                       {'product_id': product_id,
                        'subs_product_id': substitute_id})

    def saved_substitute(self):
        sql = """
select b.id, b.product_name, c.id, c.product_name
from substitute a
join product b on a.product_id = b.id
join product c on a.subs_product_id = c.id"""
        self.db.execute(sql)
        try:
            return self.db.cursor.fetchall()
        except Exception as e:
            logging.error(sql)
            logging.error(e.msg)
            return None


def has_coluns(text):
    return False if text.find(':') == -1 else True


def sql_formater(text):
    return text.replace('-', '_')

def list_to_dict(key_lst, value_lst):
    if len(key_lst) != len(value_lst):
        return None
    d = {}
    for i in range(len(key_lst)):
        d[key_lst[i]] = value_lst[i]
    return d
