# coding: utf-8
"""Setup function for purbeurre."""
from purbeurre.db.manager import Manager
from purbeurre.setup.api import OpenFoodFacts


def main():
    """Setup main."""
    manager = Manager()
    manager.setup()

    client = OpenFoodFacts()
    for product_dict in client.get_products():
        manager.insert_product(product_dict)


if __name__ == "__main__":
    main()
