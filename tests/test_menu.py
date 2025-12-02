import re
from playwright.sync_api import Page, expect
from pages.MenuPage import MenuPage


def test_adding_first_item_to_cart(new_menu_page: Page):
    """ Check that the first cup can be added to the cart by a simple click"""
    cup_number = 0
    menu_page = MenuPage(new_menu_page)
    menu_page.click_on_nth_cup(cup_number)
    expect(menu_page.cart_link).to_contain_text(f"({cup_number + 1})")

def test_hover_state(new_menu_page: Page):
    """ Check that a cup is rotated on hover"""
    cup_number = 0
    menu_page = MenuPage(new_menu_page)
    cup = menu_page.all_cups.nth(cup_number)
    expect(cup).to_have_css("transform", "none")
    menu_page.hover_over_nth_cup(cup_number)
    expect(cup).to_have_css("cursor", "pointer")
    expect(cup).to_have_css("transform", re.compile("^matrix*"))








