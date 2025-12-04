import re
import pytest
from playwright.sync_api import Page, expect
from pages.MenuPage import MenuPage


@pytest.mark.regression
def test_url(base_url, new_menu_page: Page):
    """ Check url of the menu page"""
    expect(new_menu_page).to_have_url(base_url)

@pytest.mark.failing
def test_failing_test(new_menu_page: Page):
    """ Intentionally fail the test"""
    expect(new_menu_page).to_have_url("https://invalid_url.com")

@pytest.mark.sanity
@pytest.mark.regression
def test_adding_first_item_to_cart(new_menu_page: Page):
    """ Check that the first cup can be added to the cart by a simple click"""
    cup_number = 0
    menu_page = MenuPage(new_menu_page)
    menu_page.click_on_nth_cup(cup_number)
    expect(menu_page.cart_link).to_contain_text(f"({cup_number + 1})")

@pytest.mark.regression
def test_hover_state(new_menu_page: Page):
    """ Check that a cup is rotated on hover"""
    cup_number = 0
    menu_page = MenuPage(new_menu_page)
    cup = menu_page.all_cups.nth(cup_number)
    expect(cup).to_have_css("transform", "none")
    menu_page.hover_over_nth_cup(cup_number)
    expect(cup).to_have_css("cursor", "pointer")
    expect(cup).to_have_css("transform", re.compile("^matrix*"))