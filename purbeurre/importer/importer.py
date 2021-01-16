"""Create db function for purbeurre."""
from purbeurre.db.manager import Manager
from purbeurre.importer.api import OpenFoodFacts


def main():
    """Create db and fill up MySQL database with the OpenFoodFats API.

    Retruns:
        Nothing
    """
    manager = Manager()
    manager.create_db()

    client = OpenFoodFacts()
    while client.categories:
        prods_dict_lst = client.get_products()
        if prods_dict_lst:
            for product_dict in prods_dict_lst:
                manager.insert_product(product_dict)


if __name__ == "__main__":
    main()
