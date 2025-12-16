import pytest
from playwright.sync_api import Page, expect
from pages.MenuPage import MenuPage
from utils.data_reader_util import read_all_coffee_details_from_file

all_coffee_details = read_all_coffee_details_from_file("testdata/coffee_details.json")
coffee_item_count = len([coffee_item for
                         coffee_item in all_coffee_details
                         if not "(Discounted)" in coffee_item["name"]])


@pytest.mark.sanity
@pytest.mark.regression
@pytest.mark.parametrize('cup_number', [0, (coffee_item_count - 1) // 2, coffee_item_count - 1])
def test_adding_one_coffee_to_cart(cup_number, new_menu_page: Page):
    """Check that a cup can be added to the cart by a left mouse click."""
    menu_page = MenuPage(new_menu_page)
    coffee_name = menu_page.get_nth_coffee_item_name(cup_number)
    coffee_price = menu_page.get_nth_coffee_item_price(cup_number)
    menu_page.click_on_nth_cup(cup_number)
    expect(menu_page.cart_link).to_contain_text("cart (1)")
    expect(menu_page.total_value).to_have_text(f"Total: ${coffee_price:.2f}")
    menu_page.pay_container.hover()
    expect(menu_page.cart_preview).to_contain_text(f"{coffee_name} x 1")


@pytest.mark.sanity
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
    menu_page.pay_container.hover()
    expect(menu_page.cart_preview).to_contain_text(f"{coffee_name} x 1")


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
    menu_page.pay_container.hover()
    expect(menu_page.cart_preview).not_to_be_visible()


@pytest.mark.sanity
@pytest.mark.regression
def test_adding_two_coffees_to_cart(new_menu_page: Page):
    """Check that two cups can be added to the cart and the total price is correct."""
    first_cup = 3
    second_cup = 7
    menu_page = MenuPage(new_menu_page)
    first_coffee_name = menu_page.get_nth_coffee_item_name(first_cup)
    second_coffee_name = menu_page.get_nth_coffee_item_name(second_cup)
    first_coffee_price = menu_page.get_nth_coffee_item_price(first_cup)
    second_coffee_price = menu_page.get_nth_coffee_item_price(second_cup)
    menu_page.click_on_nth_cup(first_cup)
    menu_page.click_on_nth_cup(second_cup)
    expect(menu_page.cart_link).to_contain_text("cart (2)")
    expect(menu_page.total_value).to_have_text(f"Total: ${first_coffee_price + second_coffee_price:.2f}")
    menu_page.pay_container.hover()
    expect(menu_page.cart_preview).to_contain_text(f"{first_coffee_name} x 1")
    expect(menu_page.cart_preview).to_contain_text(f"{second_coffee_name} x 1")


@pytest.mark.regression
def test_adding_coffee_from_cart_preview(new_menu_page: Page):
    """Check that coffee can be correctly added to the cart from cart preview."""
    cup_number = 4
    menu_page = MenuPage(new_menu_page)
    coffee_name = menu_page.get_nth_coffee_item_name(cup_number)
    coffee_price = menu_page.get_nth_coffee_item_price(cup_number)

    # First, add one coffee item to the cart.
    menu_page.click_on_nth_cup(cup_number)
    expect(menu_page.cart_link).to_contain_text("cart (1)")
    expect(menu_page.total_value).to_have_text(f"Total: ${coffee_price:.2f}")
    menu_page.pay_container.hover()
    expect(menu_page.cart_preview).to_contain_text(f"{coffee_name} x 1")

    # Then, add the same coffee item again from the cart preview.
    menu_page.add_from_cart_preview_by_name(coffee_name)
    expect(menu_page.cart_link).to_contain_text("cart (2)")
    expect(menu_page.total_value).to_have_text(f"Total: ${(coffee_price * 2):.2f}")
    expect(menu_page.cart_preview).to_contain_text(f"{coffee_name} x 2")
    expect(menu_page.cart_preview).to_be_visible()


@pytest.mark.regression
def test_removing_coffee_from_cart_preview(new_menu_page: Page):
    """Check that coffee can be correctly removed from the cart preview."""
    cup_number = 8
    menu_page = MenuPage(new_menu_page)
    coffee_name = menu_page.get_nth_coffee_item_name(cup_number)
    coffee_price = menu_page.get_nth_coffee_item_price(cup_number)

    # First, add one coffee item to the cart.
    menu_page.click_on_nth_cup(cup_number)
    expect(menu_page.cart_link).to_contain_text("cart (1)")
    expect(menu_page.total_value).to_have_text(f"Total: ${coffee_price:.2f}")
    menu_page.pay_container.hover()
    expect(menu_page.cart_preview).to_contain_text(f"{coffee_name} x 1")

    # Then, remove this coffee item from the cart preview.
    menu_page.remove_from_cart_preview_by_name(coffee_name)
    expect(menu_page.cart_link).to_contain_text("cart (0)")
    expect(menu_page.total_value).to_have_text("Total: $0.00")
    expect(menu_page.cart_preview).not_to_be_visible()


@pytest.mark.sanity
@pytest.mark.regression
def test_adding_and_removing_coffee_from_cart_preview(new_menu_page: Page):
    """Combine checks for adding and removing coffee from cart preview."""
    first_cup_number, second_cup_number, third_cup_number = 3, 5, 1
    menu_page = MenuPage(new_menu_page)
    first_coffee_name = menu_page.get_nth_coffee_item_name(first_cup_number)
    second_coffee_name = menu_page.get_nth_coffee_item_name(second_cup_number)
    third_coffee_name = menu_page.get_nth_coffee_item_name(third_cup_number)
    first_coffee_price = menu_page.get_nth_coffee_item_price(first_cup_number)
    second_coffee_price = menu_page.get_nth_coffee_item_price(second_cup_number)
    third_coffee_price = menu_page.get_nth_coffee_item_price(third_cup_number)
    total = first_coffee_price + second_coffee_price + third_coffee_price

    # First, add three coffee items to the cart and check expected state.
    menu_page.click_on_nth_cup(first_cup_number)
    menu_page.click_on_nth_cup(second_cup_number)
    menu_page.click_on_nth_cup(third_cup_number)
    expect(menu_page.cart_link).to_contain_text("cart (3)")
    expect(menu_page.total_value).to_have_text(f"Total: ${total:.2f}")
    menu_page.pay_container.hover()
    expect(menu_page.cart_preview).to_contain_text(f"{first_coffee_name} x 1")
    expect(menu_page.cart_preview).to_contain_text(f"{second_coffee_name} x 1")
    expect(menu_page.cart_preview).to_contain_text(f"{third_coffee_name} x 1")

    # Add some coffee items and remove another coffee item from the cart preview.
    menu_page.add_from_cart_preview_by_name(first_coffee_name)
    menu_page.add_from_cart_preview_by_name(second_coffee_name)
    menu_page.add_from_cart_preview_by_name(second_coffee_name)
    menu_page.remove_from_cart_preview_by_name(third_coffee_name)
    total = 2 * first_coffee_price + 3 * second_coffee_price

    expect(menu_page.cart_link).to_contain_text("cart (5)")
    expect(menu_page.total_value).to_have_text(f"Total: ${total:.2f}")
    expect(menu_page.cart_preview).to_contain_text(f"{first_coffee_name} x 2")
    expect(menu_page.cart_preview).to_contain_text(f"{second_coffee_name} x 3")
    expect(menu_page.cart_preview).not_to_contain_text(f"{third_coffee_name} x")


@pytest.mark.regression
def test_order_in_cart_preview(new_menu_page: Page):
    """Check that all coffee items in the cart preview are in alphabetic order."""
    menu_page = MenuPage(new_menu_page)
    for i in range(coffee_item_count):
        menu_page.click_on_nth_cup(i)
    menu_page.pay_container.hover()
    coffee_names_in_cart_preview = menu_page.get_coffee_names_in_cart_preview()
    expected_coffee_names_in_order = sorted(coffee_names_in_cart_preview)
    assert coffee_names_in_cart_preview == expected_coffee_names_in_order, \
        "Coffee items in cart preview are not in expected alphabetic order."
