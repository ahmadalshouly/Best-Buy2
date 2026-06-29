import pytest
from products import Product, NonStockedProduct, LimitedProduct
from promotions import Promotion, SecondHalfPrice, PercentDiscount, ThirdOneFree


def test_create_normal_product():
    """Test that creating a normal product works."""
    product = Product("MacBook Air M2", price=1450, quantity=100)

    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.get_quantity() == 100
    assert product.is_active() is True


def test_create_product_with_empty_name():
    """Test that an empty name raises an exception."""
    with pytest.raises(ValueError):
        Product("", price=1450, quantity=100)


def test_create_product_with_invalid_name_type():
    """Test that a non-string name raises an exception."""
    with pytest.raises(ValueError):
        Product(None, price=1450, quantity=100)


def test_create_product_with_negative_price():
    """Test that a negative price raises an exception."""
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_create_product_with_zero_price():
    """Test that a zero price raises an exception."""
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=0, quantity=100)


def test_create_product_with_zero_quantity():
    """Test that a zero quantity raises an exception."""
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=1450, quantity=0)


def test_product_becomes_inactive_at_zero_quantity():
    """Test that a product becomes inactive when quantity reaches 0."""
    product = Product("Test Product", price=100, quantity=1)
    assert product.is_active() is True

    product.buy(1)  # Buy the last unit

    assert product.get_quantity() == 0
    assert product.is_active() is False


def test_product_purchase_modifies_quantity_and_returns_total():
    """Test that buying a product modifies quantity and returns correct total."""
    product = Product("Test Product", price=100, quantity=10)

    total = product.buy(3)

    assert product.get_quantity() == 7
    assert total == 300.0


def test_buy_too_much_raises_exception():
    """Test that buying more than available raises an exception."""
    product = Product("Test Product", price=100, quantity=5)

    with pytest.raises(ValueError):
        product.buy(10)

    # Ensure quantity was not changed
    assert product.get_quantity() == 5


def test_non_stock_product_raises_exception():
    """Test that non-stock product raises an exception."""
    product = NonStockedProduct("Windows License", price=125)

    with pytest.raises(ValueError):
        product.buy(0)


def test_limited_product_buy_within_limit():
    product = LimitedProduct("Shipping", price=10, quantity=100, maximum=1)

    total = product.buy(1)

    assert total == 10.0
    assert product.get_quantity() == 99


def test_limited_product_buy_over_limit_raises_exception():
    product = LimitedProduct("Shipping", price=10, quantity=100, maximum=1)

    with pytest.raises(ValueError):
        product.buy(2)

    assert product.get_quantity() == 100


def test_set_and_get_promotion():
    product = Product("Test Product", price=100, quantity=10)

    assert product.get_promotion() is None

    promo = SecondHalfPrice("Second Half Price")
    product.set_promotion(promo)

    assert product.get_promotion() == promo


def test_percent_discount_promotion():
    product = Product("Test Product", price=100, quantity=10)
    promo = PercentDiscount("30% Off", 30)
    product.set_promotion(promo)

    total = product.buy(2)

    assert total == 140.0


def test_second_half_price_promotion():
    product = Product("Test Product", price=100, quantity=10)
    promo = SecondHalfPrice("Second Half Price")
    product.set_promotion(promo)

    total = product.buy(3)

    assert total == 250.0


def test_third_one_free_promotion():
    product = Product("Test Product", price=100, quantity=10)
    promo = ThirdOneFree("3 for 2")
    product.set_promotion(promo)

    total = product.buy(3)

    assert total == 200.0


def test_buy_with_promotion_reduces_quantity():
    product = Product("Test Product", price=100, quantity=10)
    promo = PercentDiscount("50% Off", 50)
    product.set_promotion(promo)

    product.buy(2)

    assert product.get_quantity() == 8


def test_remove_promotion():
    product = Product("Test Product", price=100, quantity=10)
    product.set_promotion(PercentDiscount("50% Off", 50))
    product.set_promotion(None)

    total = product.buy(2)

    assert total == 200.0