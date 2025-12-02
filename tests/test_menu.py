from playwright.sync_api import Page, expect


def test_adding_first_item_to_cart(page: Page):
    page.goto("https://coffee-cart.app/")
    page.locator(".cup").nth(0).click()
    expect(page.locator('a[href="/cart"]')).to_contain_text("(1)")










