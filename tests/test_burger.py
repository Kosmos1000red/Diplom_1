import pytest


class TestBurger:
    def test_ingredients_are_not_shared_between_burgers(
        self, burger, ingredient_factory
    ):
        another_burger = type(burger)()
        burger.add_ingredient(ingredient_factory("Сыр"))

        assert another_burger.ingredients == []

    def test_set_buns(self, burger, bun):
        burger.set_buns(bun)

        assert burger.bun is bun

    @pytest.mark.parametrize("count", [1, 2, 3])
    def test_add_ingredients_preserves_order(
        self, burger, ingredient_factory, count
    ):
        ingredients = [
            ingredient_factory(f"Ингредиент {index}")
            for index in range(count)
        ]

        for ingredient in ingredients:
            burger.add_ingredient(ingredient)

        assert burger.ingredients == ingredients

    def test_add_same_ingredient_twice(self, burger, ingredient_factory):
        ingredient = ingredient_factory("Сыр")

        burger.add_ingredient(ingredient)
        burger.add_ingredient(ingredient)

        assert burger.ingredients == [ingredient, ingredient]

    @pytest.mark.parametrize(
        "index, expected_indexes",
        [
            (0, [1, 2]),
            (1, [0, 2]),
            (2, [0, 1]),
        ],
    )
    def test_remove_ingredient(
        self, burger, ingredient_factory, index, expected_indexes
    ):
        ingredients = [
            ingredient_factory("Сыр"),
            ingredient_factory("Котлета"),
            ingredient_factory("Соус"),
        ]
        burger.ingredients = ingredients.copy()

        burger.remove_ingredient(index)

        assert burger.ingredients == [
            ingredients[position] for position in expected_indexes
        ]

    def test_remove_only_ingredient(self, burger, ingredient_factory):
        burger.ingredients = [ingredient_factory("Сыр")]

        burger.remove_ingredient(0)

        assert burger.ingredients == []

    @pytest.mark.parametrize(
        "index, new_index, expected_indexes",
        [
            (0, 2, [1, 2, 0]),
            (2, 0, [2, 0, 1]),
            (0, 1, [1, 0, 2]),
            (1, 1, [0, 1, 2]),
        ],
    )
    def test_move_ingredient(
        self,
        burger,
        ingredient_factory,
        index,
        new_index,
        expected_indexes,
    ):
        ingredients = [
            ingredient_factory("Сыр"),
            ingredient_factory("Котлета"),
            ingredient_factory("Соус"),
        ]
        burger.ingredients = ingredients.copy()

        burger.move_ingredient(index, new_index)

        assert burger.ingredients == [
            ingredients[position] for position in expected_indexes
        ]

    @pytest.mark.parametrize(
        "bun_price, ingredient_prices, expected_price",
        [
            (100, [], 200),
            (100, [50], 250),
            (100, [50, 25, 10], 285),
            (0, [0], 0),
            (99.9, [10.1, 20.2], 230.1),
        ],
    )
    def test_get_price(
        self,
        burger,
        bun,
        ingredient_factory,
        bun_price,
        ingredient_prices,
        expected_price,
    ):
        bun.get_price.return_value = bun_price
        burger.bun = bun
        burger.ingredients = [
            ingredient_factory(f"Ингредиент {index}", price)
            for index, price in enumerate(ingredient_prices)
        ]

        assert burger.get_price() == pytest.approx(expected_price)

    def test_get_receipt_without_ingredients(self, burger, bun):
        burger.bun = bun

        expected_receipt = (
            "(==== Булочка ====)\n"
            "(==== Булочка ====)\n"
            "\n"
            "Price: 200"
        )

        assert burger.get_receipt() == expected_receipt

    def test_get_receipt_with_ingredients(
        self, burger, bun, ingredient_factory
    ):
        burger.bun = bun
        burger.ingredients = [
            ingredient_factory("Кетчуп", 20, "SAUCE"),
            ingredient_factory("Котлета", 50, "FILLING"),
        ]

        expected_receipt = (
            "(==== Булочка ====)\n"
            "= sauce Кетчуп =\n"
            "= filling Котлета =\n"
            "(==== Булочка ====)\n"
            "\n"
            "Price: 270"
        )

        assert burger.get_receipt() == expected_receipt