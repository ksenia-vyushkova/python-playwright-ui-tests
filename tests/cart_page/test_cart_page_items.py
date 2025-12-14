from playwright.sync_api import Page, expect
from pages.CartPage import CartPage
from pages.MenuPage import MenuPage


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
    expect(cart_page.get_list_entry_for_coffee(coffee_name)).to_have_text(
        cart_page.get_row_text(coffee_name, coffee_price, 1))


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
    expect(cart_page.get_list_entry_for_coffee(coffee_name_1)).to_have_text(
        cart_page.get_row_text(coffee_name_1, coffee_price_1, 1))
    expect(cart_page.get_list_entry_for_coffee(coffee_name_2)).to_have_text(
        cart_page.get_row_text(coffee_name_2, coffee_price_2, 1))


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
    expect(cart_page.get_list_entry_for_coffee(coffee_name)).to_have_text(
        cart_page.get_row_text(coffee_name, coffee_price, 2))


def test_empty_cart(new_menu_page: Page):
    """ Check that cart is empty when no items were added."""
    menu_page = MenuPage(new_menu_page)
    cart_page = CartPage(new_menu_page)
    menu_page.cart_link.click()
    expect(cart_page.cart_list).to_be_visible()
    expect(cart_page.cart_list).to_have_text("No coffee, go add some.")


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
