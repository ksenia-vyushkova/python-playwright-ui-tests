import pytest
from playwright.sync_api import Page, expect
from pages.CartPage import CartPage
from pages.MenuPage import MenuPage
from utils.data_reader_util import read_all_coffee_details_from_file

all_coffee_details = read_all_coffee_details_from_file("testdata/coffee_details.json")
coffee_item_count = len([coffee_item for
                         coffee_item in all_coffee_details
                         if not "(Discounted)" in coffee_item["name"]])


@pytest.mark.regression
def test_one_item_in_cart(new_menu_page: Page):
    """ Check that cart shows one item when one coffee is added."""
    cup_number = 6
    menu_page = MenuPage(new_menu_page)
    cart_page = CartPage(new_menu_page)
    coffee_name = menu_page.get_nth_coffee_item_name(cup_number)
    coffee_price = menu_page.get_nth_coffee_item_price(cup_number)

    menu_page.click_on_nth_cup(cup_number)
    menu_page.cart_link.click()

    expect(cart_page.cart_link).to_contain_text("cart (1)")
    expect(cart_page.total_value).to_have_text(f"Total: ${coffee_price:.2f}")
    expect(cart_page.cart_list).to_be_visible()
    expect(cart_page.list_header_1).to_have_text("Item")
    expect(cart_page.list_header_2).to_have_text("Unit")
    expect(cart_page.list_header_3).to_have_text("Total")
    expect(cart_page.list_header_3).to_have_text("Total")
    expect(cart_page.cart_rows).to_have_count(1)
    expect(cart_page.get_list_row_for_coffee(coffee_name)).to_have_text(
        cart_page.get_row_text(coffee_name, coffee_price, 1))


@pytest.mark.regression
def test_two_items_in_cart(new_menu_page: Page):
    """ Check that cart shows two items when two coffee items are added."""
    cup_number_1, cup_number_2 = 7, 4
    menu_page = MenuPage(new_menu_page)
    cart_page = CartPage(new_menu_page)
    coffee_name_1 = menu_page.get_nth_coffee_item_name(cup_number_1)
    coffee_name_2 = menu_page.get_nth_coffee_item_name(cup_number_2)
    coffee_price_1 = menu_page.get_nth_coffee_item_price(cup_number_1)
    coffee_price_2 = menu_page.get_nth_coffee_item_price(cup_number_2)

    menu_page.click_on_nth_cup(cup_number_1)
    menu_page.click_on_nth_cup(cup_number_2)
    menu_page.cart_link.click()

    expect(cart_page.cart_link).to_contain_text("cart (2)")
    expect(cart_page.total_value).to_have_text(f"Total: ${coffee_price_1 + coffee_price_2:.2f}")
    expect(cart_page.cart_rows).to_have_count(2)
    expect(cart_page.get_list_row_for_coffee(coffee_name_1)).to_have_text(
        cart_page.get_row_text(coffee_name_1, coffee_price_1, 1))
    expect(cart_page.get_list_row_for_coffee(coffee_name_2)).to_have_text(
        cart_page.get_row_text(coffee_name_2, coffee_price_2, 1))


@pytest.mark.regression
def test_two_same_coffee_items_in_cart(new_menu_page: Page):
    """ Check that cart shows one row for a coffee item that was added twice."""
    cup_number = 2
    menu_page = MenuPage(new_menu_page)
    cart_page = CartPage(new_menu_page)
    coffee_name = menu_page.get_nth_coffee_item_name(cup_number)
    coffee_price = menu_page.get_nth_coffee_item_price(cup_number)

    menu_page.click_on_nth_cup(cup_number)
    menu_page.click_on_nth_cup(cup_number)
    menu_page.cart_link.click()

    expect(cart_page.cart_link).to_contain_text("cart (2)")
    expect(cart_page.total_value).to_have_text(f"Total: ${coffee_price * 2:.2f}")
    expect(cart_page.cart_rows).to_have_count(1)
    expect(cart_page.get_list_row_for_coffee(coffee_name)).to_have_text(
        cart_page.get_row_text(coffee_name, coffee_price, 2))


@pytest.mark.sanity
@pytest.mark.regression
def test_promo_item_in_cart(new_menu_page: Page):
    """ Check that cart shows the discounted coffee item from the promo pop up."""
    cup_number_1, cup_number_2 = 0, 8
    menu_page = MenuPage(new_menu_page)
    cart_page = CartPage(new_menu_page)
    coffee_name_1 = menu_page.get_nth_coffee_item_name(cup_number_1)
    coffee_name_2 = menu_page.get_nth_coffee_item_name(cup_number_2)
    coffee_price_1 = menu_page.get_nth_coffee_item_price(cup_number_1)
    coffee_price_2 = menu_page.get_nth_coffee_item_price(cup_number_2)

    # Add two different coffee items to the cart, with the second one added twice to trigger the promo.
    menu_page.click_on_nth_cup(cup_number_1)
    menu_page.click_on_nth_cup(cup_number_2)
    menu_page.click_on_nth_cup(cup_number_2)

    # Add the discounted coffee item from the promo pop up.
    discounted_coffee_name = menu_page.get_promo_pop_up_coffee_name()
    discounted_coffee_price = menu_page.get_promo_pop_up_coffee_price()
    menu_page.add_coffee_from_promo_pop_up()

    # Verify that the correct coffee items are in the cart.
    menu_page.cart_link.click()

    total_value = coffee_price_1 + 2 * coffee_price_2 + discounted_coffee_price

    expect(cart_page.cart_link).to_contain_text("cart (4)")
    expect(cart_page.total_value).to_have_text(f"Total: ${total_value:.2f}")
    expect(cart_page.cart_rows).to_have_count(3)
    (expect(cart_page.get_list_row_for_coffee(f"(Discounted) {discounted_coffee_name}")).to_have_text(
        cart_page.get_row_text(f"(Discounted) {discounted_coffee_name}",
                               discounted_coffee_price, 1)))
    expect(cart_page.get_list_row_for_coffee(coffee_name_1)).to_have_text(
        cart_page.get_row_text(coffee_name_1, coffee_price_1, 1))
    expect(cart_page.get_list_row_for_coffee(coffee_name_2)).to_have_text(
        cart_page.get_row_text(coffee_name_2, coffee_price_2, 2))


@pytest.mark.regression
def test_empty_cart(new_menu_page: Page):
    """ Check that cart is empty when no items were added."""
    menu_page = MenuPage(new_menu_page)
    cart_page = CartPage(new_menu_page)
    menu_page.cart_link.click()
    expect(cart_page.cart_list).to_be_visible()
    expect(cart_page.cart_list).to_have_text("No coffee, go add some.")


@pytest.mark.regression
def test_deleting_last_coffee_from_cart(new_menu_page: Page):
    """ Check that cart is empty when the last coffee item is deleted."""
    cup_number = 2
    menu_page = MenuPage(new_menu_page)
    cart_page = CartPage(new_menu_page)
    coffee_name = menu_page.get_nth_coffee_item_name(cup_number)

    menu_page.click_on_nth_cup(cup_number)
    menu_page.cart_link.click()
    cart_page.delete_coffee_from_cart_by_name(coffee_name)

    expect(cart_page.cart_list).to_be_visible()
    expect(cart_page.cart_list).to_have_text("No coffee, go add some.")


@pytest.mark.regression
def test_rows_order_in_cart(new_menu_page: Page):
    """ Check that coffee items in cart are in expected alphabetic order."""
    menu_page = MenuPage(new_menu_page)
    cart_page = CartPage(new_menu_page)

    # Add all items to the cart, including the promo item.
    for i in range(3):
        menu_page.click_on_nth_cup(i)
    menu_page.add_coffee_from_promo_pop_up()
    for j in range(3, coffee_item_count):
        menu_page.click_on_nth_cup(j)

    # Check the order of items in the cart.
    menu_page.cart_link.click()
    coffee_names_in_cart = cart_page.get_coffee_names_in_cart()
    expected_coffee_names_in_order = sorted(coffee_names_in_cart)
    assert coffee_names_in_cart == expected_coffee_names_in_order, \
        "Coffee items in cart are not in expected alphabetic order."
