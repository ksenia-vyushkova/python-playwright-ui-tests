import pytest
from playwright.sync_api import Page, expect

from pages.CartPage import CartPage
from pages.MenuPage import MenuPage


@pytest.mark.regression
def test_increasing_coffee_items_in_cart(new_menu_page: Page):
    """ Check increasing coffee item count on cart page."""
    cup_number = 2
    menu_page = MenuPage(new_menu_page)
    cart_page = CartPage(new_menu_page)
    coffee_name = menu_page.get_nth_coffee_item_name(cup_number)
    coffee_price = menu_page.get_nth_coffee_item_price(cup_number)

    menu_page.click_on_nth_cup(cup_number)
    menu_page.cart_link.click()
    cart_page.increase_coffee_count_by_name(coffee_name)

    expect(cart_page.cart_rows).to_have_count(1)
    expect(cart_page.get_list_row_for_coffee(coffee_name)).to_have_text(
        cart_page.get_row_text(coffee_name, coffee_price, 2))


@pytest.mark.regression
def test_decreasing_coffee_items_in_cart(new_menu_page: Page):
    """ Check decreasing coffee item count on cart page."""
    cup_number = 7
    menu_page = MenuPage(new_menu_page)
    cart_page = CartPage(new_menu_page)
    coffee_name = menu_page.get_nth_coffee_item_name(cup_number)
    coffee_price = menu_page.get_nth_coffee_item_price(cup_number)

    menu_page.click_on_nth_cup(cup_number)
    menu_page.click_on_nth_cup(cup_number)
    menu_page.cart_link.click()
    cart_page.decrease_coffee_count_by_name(coffee_name)

    expect(cart_page.cart_rows).to_have_count(1)
    expect(cart_page.get_list_row_for_coffee(coffee_name)).to_have_text(
        cart_page.get_row_text(coffee_name, coffee_price, 1))


@pytest.mark.regression
def test_decreasing_the_last_coffee_item_in_cart(new_menu_page: Page):
    """ Check decreasing the last coffee item on cart page."""
    cup_number = 7
    menu_page = MenuPage(new_menu_page)
    cart_page = CartPage(new_menu_page)
    coffee_name = menu_page.get_nth_coffee_item_name(cup_number)

    menu_page.click_on_nth_cup(cup_number)
    menu_page.cart_link.click()
    cart_page.decrease_coffee_count_by_name(coffee_name)

    expect(cart_page.cart_list).to_be_visible()
    expect(cart_page.cart_list).to_have_text("No coffee, go add some.")


@pytest.mark.regression
def test_removing_one_coffee_row_in_cart(new_menu_page: Page):
    """ Check deleting coffee item row in cart page."""
    cup_number = 2
    menu_page = MenuPage(new_menu_page)
    cart_page = CartPage(new_menu_page)
    coffee_name = menu_page.get_nth_coffee_item_name(cup_number)

    menu_page.click_on_nth_cup(cup_number)
    menu_page.click_on_nth_cup(cup_number)
    menu_page.cart_link.click()
    cart_page.delete_coffee_from_cart_by_name(coffee_name)

    expect(cart_page.cart_list).to_be_visible()
    expect(cart_page.cart_list).to_have_text("No coffee, go add some.")


@pytest.mark.regression
def test_combination_of_actions_on_cart_page(new_menu_page: Page):
    """ Check deleting coffee item row in cart page."""
    first_cup_number, second_cup_number, third_cup_number = 5, 1, 0
    menu_page = MenuPage(new_menu_page)
    cart_page = CartPage(new_menu_page)
    first_coffee_name = menu_page.get_nth_coffee_item_name(first_cup_number)
    second_coffee_name = menu_page.get_nth_coffee_item_name(second_cup_number)
    third_coffee_name = menu_page.get_nth_coffee_item_name(third_cup_number)
    second_coffee_price = menu_page.get_nth_coffee_item_price(second_cup_number)
    third_coffee_price = menu_page.get_nth_coffee_item_price(third_cup_number)

    menu_page.click_on_nth_cup(first_cup_number)
    menu_page.click_on_nth_cup(second_cup_number)
    menu_page.click_on_nth_cup(third_cup_number)
    menu_page.click_on_nth_cup(third_cup_number)

    menu_page.cart_link.click()
    cart_page.increase_coffee_count_by_name(second_coffee_name)
    cart_page.increase_coffee_count_by_name(second_coffee_name)
    cart_page.decrease_coffee_count_by_name(third_coffee_name)
    cart_page.delete_coffee_from_cart_by_name(first_coffee_name)

    expect(cart_page.cart_rows).to_have_count(2)
    expect(cart_page.get_list_row_for_coffee(second_coffee_name)).to_have_text(
        cart_page.get_row_text(second_coffee_name, second_coffee_price, 3))
    expect(cart_page.get_list_row_for_coffee(third_coffee_name)).to_have_text(
        cart_page.get_row_text(third_coffee_name, third_coffee_price, 1))
