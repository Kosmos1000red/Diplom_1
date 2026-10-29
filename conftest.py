from unittest.mock import Mock

import pytest

from praktikum.bun import Bun
from praktikum.burger import Burger
from praktikum.ingredient import Ingredient


@pytest.fixture
def burger():
    return Burger()


@pytest.fixture
def bun():
    bun = Mock(spec=Bun)
    bun.get_name.return_value = "Булочка"
    bun.get_price.return_value = 100
    return bun


@pytest.fixture
def ingredient_factory():
    def create(name, price=10, ingredient_type="FILLING"):
        ingredient = Mock(spec=Ingredient)
        ingredient.get_name.return_value = name
        ingredient.get_price.return_value = price
        ingredient.get_type.return_value = ingredient_type
        return ingredient

    return create