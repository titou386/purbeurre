# -*- coding: utf-8 -*-
"""database.py."""
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
            values[key] = product_dict[key]
        product_id = self.db.insert("Product", values)

        """Some tags are wrongly formatted"""
        categories_list = product_dict['categories'].split(', ')
        if len(categories_list) == 1:
            categories_list = product_dict['categories'].split(',')

        for category_name in categories_list:
            category_id = self.insert_category(category_name)
            self.insert_product_category(product_id, category_id)

    def insert_product_category(self, product_id, category_id):
        """Insert one association (product, category) in database."""
        self.db.insert("Product_category", {'product_id': product_id,
                                            'category_id': category_id})

    def insert_category(self, category_name):
        """Insert one category in database."""
        category_id = self.db.exists("Category", {'name': category_name})
        if category_id is None:
            return self.db.insert("Category", {'name': category_name})
        else:
            return category_id
