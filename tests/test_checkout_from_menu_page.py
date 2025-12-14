import pytest
from playwright.sync_api import Page, expect

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
def test_checkout_happy_path(new_menu_page: Page):
    """ Check happy path for checkout from the menu page."""
    cup_number = 6
    menu_page = MenuPage(new_menu_page)

    menu_page.click_on_nth_cup(cup_number)
    menu_page.pay_container.click()
    expect(menu_page.checkout_modal_window).to_be_visible()

    menu_page.checkout_name.fill("Test User")
    menu_page.checkout_email.fill("test@test.com")
    menu_page.checkout_promotion_agreement.check()
    menu_page.submit_order_button.click()
    expect(menu_page.checkout_modal_window).not_to_be_visible()
    expect(menu_page.successful_checkout_message).to_be_visible()
    expect(menu_page.successful_checkout_message).to_have_text(
        "Thanks for your purchase. Please check your email for payment.")
    expect(menu_page.cart_link).to_have_text("cart (0)")
    expect(menu_page.total_value).to_have_text("Total: $0.00")

@pytest.mark.regression
def test_checkout_dialog_can_be_closed(new_menu_page: Page):
    """ Check that checkout dialog can be closed."""
    cup_number = 3
    menu_page = MenuPage(new_menu_page)

    menu_page.click_on_nth_cup(cup_number)
    menu_page.pay_container.click()
    expect(menu_page.checkout_modal_window).to_be_visible()

    menu_page.close_checkout_dialog_button.click()
    expect(menu_page.checkout_modal_window).not_to_be_visible()
    expect(menu_page.successful_checkout_message).not_to_be_visible()


@pytest.mark.regression
@pytest.mark.parametrize("name, email", invalid_user_input)
def test_checkout_with_incorrect_user_input(name, email, new_menu_page: Page):
    """ Check that incorrect user input is handled properly during checkout."""
    cup_number = 0
    menu_page = MenuPage(new_menu_page)

    menu_page.click_on_nth_cup(cup_number)
    menu_page.pay_container.click()
    expect(menu_page.checkout_modal_window).to_be_visible()

    menu_page.checkout_name.fill(name)
    menu_page.checkout_email.fill(email)
    menu_page.submit_order_button.click()
    expect(menu_page.checkout_modal_window).to_be_visible()
    expect(menu_page.successful_checkout_message).not_to_be_visible()
