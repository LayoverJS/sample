import pytest
from unittest.mock import patch, MagicMock
from discounts import Discount

@pytest.fixture
def cart_mock():
    cart = MagicMock()
    cart.user_type = 'prime'
    cart.items = []
    cart.total_price = 0
    cart.calculate_total_price = MagicMock(return_value=100)
    return cart

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1, min_purchase_amount=50)

@pytest.fixture
def premium_cart_mock():
    cart = MagicMock()
    cart.user_type = 'premium'
    cart.items = [{'category': 'electronics'}]
    cart.total_price = 0
    cart.calculate_total_price = MagicMock(return_value=100)
    return cart

@pytest.fixture
def regular_cart_mock():
    cart = MagicMock()
    cart.user_type = 'regular'
    cart.items = [{'category': 'clothing'}]
    cart.total_price = 100
    cart.calculate_total_price = MagicMock(return_value=100)
    return cart

@pytest.fixture
def bulk_cart_mock():
    cart = MagicMock()
    cart.items = [{'quantity': 10, 'price': 100}]
    return cart

@pytest.fixture
def seasonal_cart_mock():
    cart = MagicMock()
    cart.total_price = 200
    cart.calculate_total_price = MagicMock(return_value=200)
    return cart

@pytest.fixture
def category_cart_mock():
    cart = MagicMock()
    cart.items = [{'category': 'clothing', 'price': 100}]
    return cart

@pytest.fixture
def loyalty_cart_mock():
    cart = MagicMock()
    cart.user_type = 'loyal'
    cart.total_price = 200
    cart.calculate_total_price = MagicMock(return_value=200)
    return cart

@pytest.fixture
def flash_sale_cart_mock():
    cart = MagicMock()
    cart.items = [{'item_id': 1, 'price': 100}]
    return cart

@pytest.fixture
def below_min_purchase_cart_mock():
    cart = MagicMock()
    cart.user_type = 'regular'
    cart.items = [{'category': 'clothing'}]
    cart.total_price = 50
    cart.calculate_total_price = MagicMock(return_value=50)
    return cart

@pytest.fixture
def insufficient_bulk_cart_mock():
    cart = MagicMock()
    cart.items = [{'quantity': 2, 'price': 100}]
    return cart

@pytest.fixture
def non_holiday_cart_mock():
    cart = MagicMock()
    cart.total_price = 200
    cart.calculate_total_price = MagicMock(return_value=200)
    return cart

@pytest.fixture
def non_specific_category_cart_mock():
    cart = MagicMock()
    cart.items = [{'category': 'electronics', 'price': 100}]
    return cart

@pytest.fixture
def non_loyal_cart_mock():
    cart = MagicMock()
    cart.user_type = 'regular'
    cart.total_price = 200
    cart.calculate_total_price = MagicMock(return_value=200)
    return cart

@pytest.fixture
def items_not_on_sale_cart_mock():
    cart = MagicMock()
    cart.items = [{'item_id': 1, 'price': 100}]
    return cart
```

# happy_path - test_apply_discount_premium_user_electronics - Test that discount is applied correctly for a premium user with electronics in cart
def test_apply_discount_premium_user_electronics(discount, premium_cart_mock):
    discount.apply_discount(premium_cart_mock)
    assert premium_cart_mock.total_price == 415.0

# happy_path - test_apply_discount_non_premium_user - Test that discount is applied correctly for a non-premium user
def test_apply_discount_non_premium_user(discount, regular_cart_mock):
    discount.apply_discount(regular_cart_mock)
    assert regular_cart_mock.total_price == 110.0

# happy_path - test_apply_bulk_discount_sufficient_quantity - Test that bulk discount is applied when quantity is sufficient
def test_apply_bulk_discount_sufficient_quantity(discount, bulk_cart_mock):
    discount.apply_bulk_discount(bulk_cart_mock, bulk_quantity=5, bulk_discount_rate=0.1)
    assert bulk_cart_mock.items[0]['price'] == 90.0

# happy_path - test_apply_seasonal_discount_holiday - Test that seasonal discount is applied during holiday season
def test_apply_seasonal_discount_holiday(discount, seasonal_cart_mock):
    discount.apply_seasonal_discount(seasonal_cart_mock, season='holiday', seasonal_discount_rate=0.2)
    assert seasonal_cart_mock.total_price == 160.0

# happy_path - test_apply_category_discount_specific_category - Test that category discount is applied to specified category
def test_apply_category_discount_specific_category(discount, category_cart_mock):
    discount.apply_category_discount(category_cart_mock, category='clothing', category_discount_rate=0.2)
    assert category_cart_mock.items[0]['price'] == 80.0

# happy_path - test_apply_flash_sale_discount_items_on_sale - Test that flash sale discount is applied to items on sale
def test_apply_flash_sale_discount_items_on_sale(discount, flash_sale_cart_mock):
    discount.apply_flash_sale_discount(flash_sale_cart_mock, flash_sale_rate=0.2, items_on_sale=[1])
    assert flash_sale_cart_mock.items[0]['price'] == 80.0

# edge_case - test_apply_discount_below_min_purchase - Test that no discount is applied when total price is below minimum purchase amount
def test_apply_discount_below_min_purchase(discount, below_min_purchase_cart_mock):
    discount.apply_discount(below_min_purchase_cart_mock)
    assert below_min_purchase_cart_mock.total_price == 50.0

# edge_case - test_apply_bulk_discount_insufficient_quantity - Test that no bulk discount is applied when quantity is insufficient
def test_apply_bulk_discount_insufficient_quantity(discount, insufficient_bulk_cart_mock):
    discount.apply_bulk_discount(insufficient_bulk_cart_mock, bulk_quantity=5, bulk_discount_rate=0.1)
    assert insufficient_bulk_cart_mock.items[0]['price'] == 100.0

# edge_case - test_apply_seasonal_discount_non_holiday - Test that no seasonal discount is applied during non-holiday season
def test_apply_seasonal_discount_non_holiday(discount, non_holiday_cart_mock):
    discount.apply_seasonal_discount(non_holiday_cart_mock, season='spring', seasonal_discount_rate=0.2)
    assert non_holiday_cart_mock.total_price == 200.0

# edge_case - test_apply_category_discount_non_specific_category - Test that no category discount is applied to non-specified category
def test_apply_category_discount_non_specific_category(discount, non_specific_category_cart_mock):
    discount.apply_category_discount(non_specific_category_cart_mock, category='clothing', category_discount_rate=0.2)
    assert non_specific_category_cart_mock.items[0]['price'] == 100.0

# edge_case - test_apply_loyalty_discount_non_loyal_user - Test that no loyalty discount is applied for non-loyal users
def test_apply_loyalty_discount_non_loyal_user(discount, non_loyal_cart_mock):
    discount.apply_loyalty_discount(non_loyal_cart_mock, loyalty_years=1, loyalty_discount_rate=0.1)
    assert non_loyal_cart_mock.total_price == 200.0

# edge_case - test_apply_flash_sale_discount_items_not_on_sale - Test that no flash sale discount is applied to items not on sale
def test_apply_flash_sale_discount_items_not_on_sale(discount, items_not_on_sale_cart_mock):
    discount.apply_flash_sale_discount(items_not_on_sale_cart_mock, flash_sale_rate=0.2, items_on_sale=[2])
    assert items_not_on_sale_cart_mock.items[0]['price'] == 100.0

