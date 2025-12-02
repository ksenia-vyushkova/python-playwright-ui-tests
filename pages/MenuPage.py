from playwright.sync_api import Page


class MenuPage:

    def __init__(self, page: Page):
        self.page = page

        self.cart_link = self.page.locator('a[href="/cart"]')
        self.all_cups = self.page.locator(".cup")

    def navigate(self):
        self.page.goto("https://coffee-cart.app/")

    def click_on_nth_cup(self, cupNumber):
        self.all_cups.nth(cupNumber).click()

    def hover_over_nth_cup(self, cupNumber):
        self.all_cups.nth(cupNumber).hover()