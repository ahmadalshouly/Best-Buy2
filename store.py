""" Author: Ahmad
Store Class """
from typing import List
from products import Product

class Store:
    """ Store Class """
    def __init__(self, products: List[Product]):
        """ Initialize the store """
        self.products = products

    def add_product(self, product: Product):
        """ Add a product to the store """
        self.products.append(product)

    def remove_product(self, product: Product):
        """ Remove a product from the store """
        if product in self.products:
            self.products.remove(product)

    def get_total_quantity(self) -> int:
        """ Return the total quantity of the store """
        return sum(product.get_quantity() for product in self.products)

    def get_all_products(self) -> List[Product]:
        """ Return a list of all products in the store """
        return [product for product in self.products if product.is_active()]

    def order(self, shopping_list: List[tuple]) -> float:
        """ Return the total price of the store """
        total_price = 0.0

        for product, quantity in shopping_list:
            if not product.is_active():
                raise ValueError(f"{product.name} is not available")
            if quantity > product.get_quantity():
                raise ValueError(f"Not enough {product.name} in stock")

            total_price += product.buy(quantity)

        return total_price