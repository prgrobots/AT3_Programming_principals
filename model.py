# product_manager.py
from database import fruit_veg_database

class Model:
    def __init__(self):
        self.products = fruit_veg_database

    def load_data(self):
        # In this simplified version, we won't actually load data from a file
        # Since we're using the in-memory database
        pass

    def save_data(self):
        # In this simplified version, we won't actually save data to a file
        pass

    def get_products(self):
        return self.products

    def add_or_update_product(self, product_name, price, emoji):
        self.products[product_name] = {
            'name': product_name,
            'price': price,
            'emoji': emoji,
            'description': product_name
        }
