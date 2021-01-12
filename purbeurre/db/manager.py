"""manager.py."""
import purbeurre.db.database
import logging


class Manager:
    """Class manager."""

    def __init__(self):
        """Create an mysql instance."""
        self.db = purbeurre.db.database.Mysql()

    def create_db(self):
        """Database initialisation.

        Apply structure from structure.sql file.
        """
        self.db.apply_structure()

    def insert_product(self, product_dict):
        """Insert one product in database.

        Parameters:
            product_dict(dict): Contains all tags from
                openfoodfacts api. Some tags are selected for the
                product insertion.

        Returns:
            Nothing.
        """
        values = {}
        for key in ('code',
                    'product_name',
                    'generic_name',
                    'quantity',
                    'nutriscore_grade',
                    'nutriments:energy-kcal_100g',
                    'nutriments:fat_100g',
                    'nutriments:saturated-fat_100g',
                    'nutriments:carbohydrates_100g',
                    'nutriments:sugars_100g',
                    'nutriments:fiber_100g',
                    'nutriments:proteins_100g',
                    'nutriments:salt_100g',
                    'nutriments:nova-group',
                    'nutriments:energy_kcal_unit',
                    'nutriments:fat_unit',
                    'nutriments:saturated_fat_unit',
                    'nutriments:carbohydrates_unit',
                    'nutriments:sugars_unit',
                    'nutriments:fiber_unit',
                    'nutriments:proteins_unit',
                    'nutriments:salt_unit'
                    ):
            try:
                # Somes tags are missing or empty and can be replaced
                if key == 'product_name' or key == 'generic_name':
                    if key not in product_dict:
                        values[key] = product_dict[key + '_fr']
                    elif product_dict[key] == '':
                        values[key] = product_dict[key + '_fr']
                    else:
                        values[key] = product_dict[key]
                    values[key] = values[key].replace('\n', ' ')
                elif has_colun(key):
                    key1, key2 = key.split(':')
                    values[sql(key2)] = product_dict[key1][key2]
                else:
                    values[key] = product_dict[key]
            except KeyError:
                pass

        product_id = self.db.insert("product", values)
        if not product_id:
            return

        # Categories, countries and stores insertion.
        for key in ("categories", "categories_old", "countries", "stores"):
            try:
                # Some values in key are wrongly formatted
                product_dict[key] = product_dict[key].replace('\n', ' ')
                for pattern in (', ', ',', '  ', ' - '):
                    val_list = product_dict[key].split(pattern)
                    if len(val_list) > 1:
                        break

                # Re-check every items list
                copy = val_list.copy()
                for val in copy:
                    for pattern in (', ', ',', '  ', ' - '):
                        tmp = val.split(pattern)
                        if len(tmp) > 1:
                            val_list.remove(val)
                            for t in tmp:
                                val_list.append(t)
                            break

                for value in val_list:
                    if has_colun(value):
                        value = value[3:]
                    if key == "categories" or key == "categories_old":
                        index = self.insert_category(value)
                        if index:
                            self.insert_product_category(product_id, index)
                    elif key == "countries":
                        index = self.insert_country(value)
                        if index:
                            self.insert_product_country(product_id, index)
                    elif key == "stores":
                        index = self.insert_store(value)
                        if index:
                            self.insert_product_store(product_id, index)
            except KeyError:
                pass

    def insert_product_category(self, product_id, category_id):
        """Insert one association (product, category) in database.

        Parameters:
            product_id(int/str): Product index
            category_id(int/str): Category index

        Returns:
            Nothing
        """
        if not self.db.get("product_category", {'product_id': product_id,
                                                'category_id': category_id}):
            self.db.insert("product_category", {'product_id': product_id,
                                                'category_id': category_id})

    def insert_category(self, category_name):
        """Insert one category in database.

        Parameters:
            category_name(str): Category should be inserted

        Returns:
            int: Return an index
        """
        return self.db.insert("category", {'name': category_name})

    def insert_product_country(self, product_id, country_id):
        """Insert one association (product, country) in database.

        Parameters:
            product_id(int/str): Product index
            country_id(int/str): Country index

        Returns:
            Nothing
        """
        self.db.insert("product_country", {'product_id': product_id,
                                           'country_id': country_id})

    def insert_country(self, country_name):
        """Insert one country in database.

        Parameters:
            country_name(str): Category should be inserted

        Returns:
            int: Return an index
        """
        return self.db.insert("country", {'name': country_name})

    def insert_product_store(self, product_id, store_id):
        """Insert one association (product, store) in database.

        Parameters:
            product_id(int/str): Product index
            store_id(int/str) Store index

        Returns:
            Nothing
        """
        self.db.insert("product_store", {'product_id': product_id,
                                         'store_id': store_id})

    def insert_store(self, store_name):
        """Insert one store in database.

        Parameters:
            store_name(str): Store should be inserted

        Returns:
            int: Return an index
        """
        return self.db.insert("store", {'name': store_name})

    def search_category_name(self, search):
        """Search any patten in category name.

        Parameters:
            search(str): Search pattern in category name.

        Returns:
            Return a list of tuples (index, category name)
        """
        value = ["%{}%".format(search)]
        return self.db.query("category", value, where="name", like=True)

    def delete_substitute(self, product_id):
        """Delete a substitute by product_id.

        Parameters:
            product_id(int/str): Delete one saved substitution by index

        Returns:
            Nothing
        """
        self.db.delete('substitution',
                       {'product_id': product_id})

    def get_product_subtitution(self, product_id):
        """Search a better, if possible, or equivalent substitute.

        Parameters:
            product_id(int/str): Product index

        Returns:
            int: Return a product index for the substitution.
        """
        cat = [c[0] for c in self.db.query('product_category',
                                           (product_id,),
                                           select='category_id',
                                           where='product_id=%s')]

        sql = """
SELECT product_category.product_id
FROM product_category
JOIN product ON product.id = product_category.product_id
WHERE product_category.category_id IN ({})
    AND NOT product_category.product_id=%s
    AND product.nutriscore_grade <= (
        SELECT nutriscore_grade from product where id=%s)
    AND product.nova_group <= (
        SELECT nova_group from product where id=%s)
"""

        data_quantity = ', '.join(['%s' for e in range(len(cat))])
        sql = sql.format(data_quantity)
        cat.append(product_id)
        cat.append(product_id)
        cat.append(product_id)

        self.db.execute(sql, cat)
        try:
            prod = [p[0] for p in self.db.cursor.fetchall()]
        except Exception as e:
            logging.error('manager.py:get_product_subtitution:{}'.format(sql))
            logging.error('manager.py:get_product_subtitution:{}'.
                          format(e.msg))
            return None

        if not prod:
            return None

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

        result = [p[0] for p in self.db.query('product',
                                              occurence[index],
                                              select='id',
                                              where='id',
                                              inside=True,
                                              order='nutriscore_grade, \
                                              nova_group',
                                              limit=1)]

        if not result:
            return None
        else:
            return result[0]

    def product_in_category(self, category_id):
        """Return a list of tuples (id(int), product name(str)) in this category.

        Parameters:
            category_id(int/str): Category index
        """
        results = self.db.query("product",
                                (category_id,),
                                select="product.id, product.product_name",
                                join=("product_category",),
                                on=("product.id=product_category.product_id",),
                                where="product_category.category_id=%s")

        return self.del_duplicate_product_name(results)

    def search_product_name(self, search):
        """Search any patten in product name.

        Parameters:
            search(str): Search pattern in product name.
        Return a list of tuples (id, name)
        """
        value = ("%{}%".format(search),)
        return self.del_duplicate_product_name(self.db.query("product", value,
                                               select="id, product_name",
                                               where="product_name",
                                               like=True))

    def del_duplicate_product_name(self, products):
        """Elimine duplicate product name.

        Parameters:
        """
        prod_name = [item[1].lower() for item in products]
        for i, item in enumerate(products):
            if prod_name.count(item[1].lower()) > 1:
                quantity = self.db.query("product",
                                         (item[0],),
                                         select="quantity",
                                         where="id=%s")
                try:
                    products[i] = (item[0], item[1] + ' ' + quantity[0][0])
                except TypeError:
                    pass
        return products

    def product_detail(self, product_id):
        """Return all details of one product.

        Parameters:
            product_id(int/str): Product index.

        Returns:
            list: a list detailled of one product/
        """
        return self.db.query("product",
                             (product_id,),
                             select="""
product.id,
product.product_name,
product.generic_name,
product.quantity,
group_concat(DISTINCT store.name SEPARATOR ', '),
group_concat(DISTINCT country.name SEPARATOR ', '),
product.energy_kcal_100g, product.energy_kcal_unit,
product.fat_100g, product.fat_unit,
product.saturated_fat_100g, product.saturated_fat_unit,
product.carbohydrates_100g, product.carbohydrates_unit,
product.sugars_100g, product.sugars_unit,
product.fiber_100g, product.fiber_unit,
product.proteins_100g, product.proteins_unit,
product.salt_100g, product.salt_unit,
product.nutriscore_grade,
product.nova_group,
product.code""",
                             join=("product_store", "store",
                                   "product_country", "country"),
                             on=("product.id=product_store.product_id",
                                 "product_store.store_id=store.id",
                                 "product.id=product_country.product_id",
                                 "product_country.country_id=country.id"),
                             where="product.id=%s")[0]

    def save_substitute(self, product_id, substitute_id):
        """Save one substitution.

        Parameters:
            product_id(int/str): Product index.
            substitution_id(int/str): Product substitute
        """
        self.db.insert('substitution',
                       {'product_id': product_id,
                        'subs_product_id': substitute_id})

    def substitution_saved(self):
        """List all substitutions.

        Return a list of tuples (id prod, name prod, id sub, name sub)
        """
        return self.db.query("substitution a", None,
                             select="b.id, b.product_name, \
                                     c.id, c.product_name",
                             join=("product b", "product c"),
                             on=("a.product_id = b.id",
                                 "subs_product_id = c.id")
                             )


def has_colun(text):
    """Test if a ':' is in this string.

    Return true or false
    """
    return False if text.find(':') == -1 else True


def sql(text):
    """Replace some characters for sql language.

    Returns:
        str: return text variable with caracters replaced
    """
    return text.replace('-', '_')
