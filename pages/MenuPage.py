from playwright.sync_api import Page


class MenuPage:

    def __init__(self, page: Page):
        self.page = page

        self.cart_link = self.page.locator('a[href="/cart"]')
        self.all_cups = self.page.locator(".cup")

    def click_on_nth_cup(self, cup_number):
        self.all_cups.nth(cup_number).click()

    def hover_over_nth_cup(self, cup_number):
        self.all_cups.nth(cup_number).hover()