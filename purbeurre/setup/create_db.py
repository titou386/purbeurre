"""Setup function for purbeurre."""
from purbeurre.db.manager import Manager
from purbeurre.setup.api import OpenFoodFacts


def main():
    """Setup main."""
    manager = Manager()
    manager.setup()

    client = OpenFoodFacts()
    while client.categories:
        prods_dict_lst = client.get_products()
        for product_dict in prods_dict_lst:
            manager.insert_product(product_dict)


if __name__ == "__main__":
    main()