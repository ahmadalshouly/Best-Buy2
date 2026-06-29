"""
    Author: Ahmad
    This is the Product class"""

class Product:
    """ Product class"""
    def __init__(self, name, price, quantity):

        if not name or not isinstance(name, str):
            raise ValueError("Product Name must be a non-empty string")

        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Product Price must be a non-negative integer")

        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Product Quantity must be a non-negative integer")

        self.name = name
        self.price = price
        self.quantity = quantity
        self._active = True
        self.promotion = None

    def get_quantity(self) -> int:
        """ Returns the quantity of the product """
        return self.quantity

    def set_quantity(self, quantity):
        """ Sets the quantity of the product """
        self.quantity = quantity
        if self.quantity == 0:
            self._active = False

    def is_active(self) -> bool:
        """ Returns whether the product is active """
        return self._active

    def activate(self):
        """ Activate the product """
        self._active = True

    def deactivate(self):
        """ Deactivate the product """
        self._active = False

    def get_promotion(self):
        """ Returns the current promotion of the product (or None) """
        return self.promotion

    def set_promotion(self, promotion):
        """ Sets (or removes, by passing None) the promotion of the product """
        self.promotion = promotion

    def show(self):
        """ Show the product """
        promo_text = f", Promotion: {self.promotion.name}" if self.promotion else ""
        print(f"{self.name}, Price: {self.price}, Quantity: {self.quantity}{promo_text}")

    def buy(self, quantity):
        """Buys a given quantity of the product"""
        if quantity <= 0:
            raise ValueError("Purchase quantity must be positive")

        if quantity > self.quantity:
            raise ValueError(f"Not enough stock. Available: {self.quantity}")

        if self.promotion is not None:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = self.price * quantity

        self.quantity -= quantity

        if self.quantity == 0:
            self._active = False

        return total_price


class NonStockedProduct(Product):
    """
    Represents a non-physical product whose quantity is not tracked
    (e.g. a software license). Quantity is always 0 and stays 0.
    """


    def __init__(self, name, price):
        super().__init__(name, price, 1)
        self.quantity = 0


    def set_quantity(self, quantity):
        """ Quantity is always forced to zero for non-stocked products """
        self.quantity = 0


    def buy(self, quantity):
        """ Buys the product without touching quantity (unlimited stock) """
        if quantity <= 0:
            raise ValueError("Purchase quantity must be positive")

        if self.promotion is not None:
            return self.promotion.apply_promotion(self, quantity)
        return self.price * quantity


    def show(self):
        """ Show the product, indicating it is not stock-tracked """
        promo_text = f", Promotion: {self.promotion.name}" if self.promotion else ""
        print(f"{self.name}, Price: {self.price}, Quantity: Unlimited (Non-Stocked){promo_text}")


class LimitedProduct(Product):
    """
    Represents a product that can only be purchased up to a maximum
    quantity per order (e.g. a one-time shipping fee).
    """

    def __init__(self, name, price, quantity, maximum):
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def buy(self, quantity):
        """ Buys the product, enforcing the per-order maximum """
        if quantity > self.maximum:
            raise ValueError(
                f"Cannot purchase more than {self.maximum} of '{self.name}' per order"
            )
        return super().buy(quantity)

    def show(self):
        """ Show the product, including its per-order maximum """
        promo_text = f", Promotion: {self.promotion.name}" if self.promotion else ""
        print(
            f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, "
            f"Maximum per order: {self.maximum}{promo_text}"
        )