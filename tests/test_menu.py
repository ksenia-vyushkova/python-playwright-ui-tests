from playwright.sync_api import Page, expect
from pages.MenuPage import MenuPage


def test_adding_first_item_to_cart(page: Page):
    menu_page = MenuPage(page)
    menu_page.navigate()
    menu_page.click_on_nth_cup(0)
    expect(menu_page.cart_link).to_contain_text("(1)")










