import pytest
from playwright.sync_api import expect, Page

from pages.CartPage import CartPage
from pages.MenuPage import MenuPage

invalid_user_input = [
    ("", ""),
    ("", "test"),
    ("", "test@test.com"),
    ("Test", ""),
    ("Test", "test"),
    ("Test", "test@"),
]


@pytest.mark.regression
def test_cart_checkout_happy_path(new_menu_page: Page):
    """ Check happy path for checkout from the cart page."""
    cup_number = 3
    menu_page = MenuPage(new_menu_page)
    cart_page = CartPage(new_menu_page)

    menu_page.click_on_nth_cup(cup_number)
    menu_page.cart_link.click()
    cart_page.total_value.click()
    expect(cart_page.checkout_modal_window).to_be_visible()

    cart_page.checkout_name.fill("Test User")
    cart_page.checkout_email.fill("test@test.com")
    cart_page.checkout_promotion_agreement.check()
    cart_page.submit_order_button.click()
    expect(cart_page.checkout_modal_window).not_to_be_visible()
    expect(cart_page.successful_checkout_message).to_be_visible()
    expect(cart_page.successful_checkout_message).to_have_text(
        "Thanks for your purchase. Please check your email for payment.")
    expect(cart_page.cart_link).to_have_text("cart (0)")
    expect(cart_page.total_value).to_have_text("Total: $0.00")


@pytest.mark.regression
def test_cart_checkout_dialog_can_be_closed(new_menu_page: Page):
    """ Check that checkout dialog can be closed on cart page."""
    cup_number = 6
    menu_page = MenuPage(new_menu_page)
    cart_page = CartPage(new_menu_page)

    menu_page.click_on_nth_cup(cup_number)
    menu_page.cart_link.click()
    cart_page.total_value.click()
    expect(cart_page.checkout_modal_window).to_be_visible()

    cart_page.close_checkout_dialog_button.click()
    expect(cart_page.checkout_modal_window).not_to_be_visible()
    expect(cart_page.successful_checkout_message).not_to_be_visible()


@pytest.mark.regression
@pytest.mark.parametrize("name, email", invalid_user_input)
def test_cart_checkout_with_incorrect_user_input(name, email, new_menu_page: Page):
    """ Check that incorrect user input is handled properly during checkout from cart page."""
    cup_number = 8
    menu_page = MenuPage(new_menu_page)
    cart_page = CartPage(new_menu_page)

    menu_page.click_on_nth_cup(cup_number)
    menu_page.cart_link.click()
    cart_page.total_value.click()
    expect(cart_page.checkout_modal_window).to_be_visible()

    cart_page.checkout_name.fill(name)
    cart_page.checkout_email.fill(email)
    cart_page.submit_order_button.click()
    expect(cart_page.checkout_modal_window).to_be_visible()
    expect(cart_page.successful_checkout_message).not_to_be_visible()
