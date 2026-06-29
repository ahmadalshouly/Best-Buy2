"""
    Author: Ahmad
    This module contains the Promotion class and its subclasses.
"""

from abc import ABC, abstractmethod


class Promotion(ABC):
    """
    Abstract base class for all promotions.
    Every promotion has a name and must implement apply_promotion().
    """

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        """
        Calculates and returns the total price for buying `quantity`
        of `product`, after the promotion has been applied.
        """
        pass


class PercentDiscount(Promotion):
    """Gives a fixed percentage discount on the total price."""

    def __init__(self, name, percent):
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity) -> float:
        total_price = product.price * quantity
        return total_price * (1 - self.percent / 100)


class SecondHalfPrice(Promotion):
    """Every second item bought is sold at half price."""

    def apply_promotion(self, product, quantity) -> float:
        half_price_items = quantity // 2
        full_price_items = quantity - half_price_items
        return (full_price_items * product.price) + (half_price_items * product.price * 0.5)


class ThirdOneFree(Promotion):
    """Buy two of an item, get a third one free."""

    def apply_promotion(self, product, quantity) -> float:
        free_items = quantity // 3
        paid_items = quantity - free_items
        return paid_items * product.price