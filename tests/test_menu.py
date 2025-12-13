import pytest
from playwright.sync_api import Page, expect
from pages.MenuPage import MenuPage
from utils.data_reader_util import read_all_coffee_details_from_file

all_coffee_details = read_all_coffee_details_from_file("testdata/coffee_details.json")
coffee_item_count = len([coffee_item for
                         coffee_item in all_coffee_details
                         if not "(Discounted)" in coffee_item["name"]])


@pytest.mark.regression
def test_url_and_title(base_url, new_menu_page: Page):
    """Check url and title of the menu page."""
    expect(new_menu_page).to_have_url(base_url)
    expect(new_menu_page).to_have_title("Coffee cart")


@pytest.mark.regression
def test_default_cart_counter_and_total(new_menu_page: Page):
    """Check that default values of cart counter and 'Total' are zero."""
    menu_page = MenuPage(new_menu_page)
    expect(menu_page.cart_link).to_have_text("cart (0)")
    expect(menu_page.total_value).to_have_text("Total: $0.00")


@pytest.mark.sanity
@pytest.mark.regression
@pytest.mark.parametrize('cup_number', [0, (coffee_item_count - 1) // 2, coffee_item_count - 1])
def test_adding_one_coffee_to_cart(cup_number, new_menu_page: Page):
    """Check that a cup can be added to the cart by a left mouse click."""
    menu_page = MenuPage(new_menu_page)
    coffee_price = menu_page.get_nth_coffee_item_price(cup_number)
    menu_page.click_on_nth_cup(cup_number)
    expect(menu_page.cart_link).to_contain_text("cart (1)")
    expect(menu_page.total_value).to_have_text(f"Total: ${coffee_price:.2f}")


@pytest.mark.regression
def test_adding_one_coffee_to_cart_with_right_click(new_menu_page: Page):
    """Check that a cup can be added to the cart by a right mouse click."""
    cup_number = 6
    menu_page = MenuPage(new_menu_page)
    coffee_name = menu_page.get_nth_coffee_item_name(cup_number)
    coffee_price = menu_page.get_nth_coffee_item_price(cup_number)
    menu_page.right_click_on_nth_cup(cup_number)
    expect(menu_page.add_coffee_to_cart_question).to_have_text(f"Add {coffee_name} to the cart?")
    menu_page.agree_to_add_to_cart()
    expect(menu_page.add_coffee_to_cart_question).not_to_be_visible()
    expect(menu_page.cart_link).to_contain_text("cart (1)")
    expect(menu_page.total_value).to_have_text(f"Total: ${coffee_price:.2f}")


@pytest.mark.regression
def test_refusing_to_add_coffee_to_cart(new_menu_page: Page):
    """Check that a cup is not added to the cart when refusing the "add to cart" question."""
    cup_number = 4
    menu_page = MenuPage(new_menu_page)
    coffee_name = menu_page.get_nth_coffee_item_name(cup_number)
    menu_page.right_click_on_nth_cup(cup_number)
    expect(menu_page.add_coffee_to_cart_question).to_have_text(f"Add {coffee_name} to the cart?")
    menu_page.refuse_to_add_to_cart()
    expect(menu_page.add_coffee_to_cart_question).not_to_be_visible()
    expect(menu_page.cart_link).to_contain_text("cart (0)")
    expect(menu_page.total_value).to_have_text("Total: $0.00")


@pytest.mark.sanity
@pytest.mark.regression
def test_adding_two_coffees_to_cart(new_menu_page: Page):
    """Check that two cups can be added to the cart and the total price is correct."""
    first_cup = 3
    second_cup = 7
    menu_page = MenuPage(new_menu_page)
    first_coffee_price = menu_page.get_nth_coffee_item_price(first_cup)
    second_coffee_price = menu_page.get_nth_coffee_item_price(second_cup)
    menu_page.click_on_nth_cup(first_cup)
    menu_page.click_on_nth_cup(second_cup)
    expect(menu_page.cart_link).to_contain_text("cart (2)")
    expect(menu_page.total_value).to_have_text(f"Total: ${first_coffee_price + second_coffee_price:.2f}")
