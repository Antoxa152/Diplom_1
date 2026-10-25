import pytest
import allure
from unittest.mock import MagicMock
from burger import Burger


@allure.title("Проверка установки булочек в бургер")
@allure.description("Убедиться, что set_buns корректно сохраняет булочку в атрибуте bun")
def test_set_buns():
    mock_bun = MagicMock()
    mock_bun.get_name.return_value = "Classic Bun"
    mock_bun.get_price.return_value = 50.0

    burger = Burger()
    burger.set_buns(mock_bun)

    assert burger.bun is mock_bun


@pytest.mark.parametrize(
    "ingredients_count,expected_price",
    [
        (0, 100.0),   
        (1, 120.0),   
        (3, 160.0),   
    ],
)
@allure.title("Расчёт цены бургера с разным количеством ингредиентов")
@allure.description("Проверить get_price для разного количества ингредиентов при фиксированной цене булочки и ингредиента")
def test_get_price_parametrized(ingredients_count: int, expected_price: float):
    
    mock_bun = MagicMock()
    mock_bun.get_name.return_value = "Mock Bun"
    mock_bun.get_price.return_value = 50.0  # цена одной булочки

    mock_ingredient = MagicMock()
    mock_ingredient.get_type.return_value = "filling"
    mock_ingredient.get_name.return_value = "Cheese"
    mock_ingredient.get_price.return_value = 20.0

    burger = Burger()
    burger.set_buns(mock_bun)
    for _ in range(ingredients_count):
        burger.add_ingredient(mock_ingredient)

    assert burger.get_price() == expected_price


@allure.title("Добавление ингредиента в бургер")
@allure.description("Проверить, что add_ingredient корректно добавляет ингредиент в список")
def test_add_ingredient():
    mock_ingredient_1 = MagicMock()
    mock_ingredient_1.get_type.return_value = "sauce"
    mock_ingredient_1.get_name.return_value = "Ketchup"
    mock_ingredient_1.get_price.return_value = 15.0

    mock_ingredient_2 = MagicMock()
    mock_ingredient_2.get_type.return_value = "filling"
    mock_ingredient_2.get_name.return_value = "Beef"
    mock_ingredient_2.get_price.return_value = 40.0

    burger = Burger()
    burger.add_ingredient(mock_ingredient_1)
    burger.add_ingredient(mock_ingredient_2)

    assert len(burger.ingredients) == 2
    assert burger.ingredients[0] is mock_ingredient_1
    assert burger.ingredients[1] is mock_ingredient_2


@allure.title("Удаление ингредиента по индексу")
@allure.description("Проверить remove_ingredient: удаление по валидному индексу и отсутствие ошибки при выходе за границы (если логика допускает)")
def test_remove_ingredient():
    mock_ingredient_1 = MagicMock()
    mock_ingredient_1.get_type.return_value = "filling"
    mock_ingredient_1.get_name.return_value = "Beef"
    mock_ingredient_1.get_price.return_value = 40.0

    mock_ingredient_2 = MagicMock()
    mock_ingredient_2.get_type.return_value = "vegetable"
    mock_ingredient_2.get_name.return_value = "Lettuce"
    mock_ingredient_2.get_price.return_value = 10.0

    burger = Burger()
    burger.add_ingredient(mock_ingredient_1)
    burger.add_ingredient(mock_ingredient_2)

    burger.remove_ingredient(0)

    assert len(burger.ingredients) == 1
    assert burger.ingredients[0] is mock_ingredient_2

    burger.remove_ingredient(0)
    assert len(burger.ingredients) == 0


@allure.title("Перемещение ингредиента внутри списка")
@allure.description("Проверить move_ingredient: корректное изменение порядка элементов")
def test_move_ingredient():
    mocks = [MagicMock() for _ in range(3)]
    for m in mocks:
        m.get_type.return_value = "filling"
        m.get_name.return_value = "Ing"
        m.get_price.return_value = 10.0

    burger = Burger()
    for m in mocks:
        burger.add_ingredient(m)

        burger.move_ingredient(0, 2)

    assert burger.ingredients == [mocks[1], mocks[2], mocks[0]]

    burger.move_ingredient(2, 0)
    assert burger.ingredients == [mocks[0], mocks[1], mocks[2]]


@allure.title("Формирование чека (get_receipt)")
@allure.description("Проверить формат и содержимое строки чека, включая названия, типы и итоговую цену")
def test_get_receipt():
    mock_bun = MagicMock()
    mock_bun.get_name.return_value = "Premium Bun"
    mock_bun.get_price.return_value = 60.0

    mock_ingr_1 = MagicMock()
    mock_ingr_1.get_type.return_value = "FILLING"
    mock_ingr_1.get_name.return_value = "Chicken"
    mock_ingr_1.get_price.return_value = 70.0

    mock_ingr_2 = MagicMock()
    mock_ingr_2.get_type.return_value = "SAUCE"
    mock_ingr_2.get_name.return_value = "Garlic"
    mock_ingr_2.get_price.return_value = 25.0

    burger = Burger()
    burger.set_buns(mock_bun)
    burger.add_ingredient(mock_ingr_1)
    burger.add_ingredient(mock_ingr_2)

    receipt = burger.get_receipt()

    lines = receipt.splitlines()
    assert lines[0] == "(==== Premium Bun ===="
    assert "= filling chicken =" in lines[1].lower()
    assert "= sauce garlic =" in lines[2].lower()
    assert lines[3] == "(==== Premium Bun ===="

    assert "Price: 215.0" in receipt


@allure.title("Чек для бургера без ингредиентов")
@allure.description("Проверить get_receipt при пустом списке ингредиентов")
def test_get_receipt_empty_ingredients():
    mock_bun = MagicMock()
    mock_bun.get_name.return_value = "Basic Bun"
    mock_bun.get_price.return_value = 30.0

    burger = Burger()
    burger.set_buns(mock_bun)

    receipt = burger.get_receipt()
    lines = receipt.splitlines()

    assert lines[0] == "(==== Basic Bun ===="
    assert lines[1] == "(==== Basic Bun ===="
    assert "Price: 60.0" in receipt
