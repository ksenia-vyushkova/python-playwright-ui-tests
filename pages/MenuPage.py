from playwright.sync_api import Page


class MenuPage:

    def __init__(self, page: Page):
        self.page = page

        self.cart_link = self.page.locator('a[href="/cart"]')
        self.all_cups = self.page.locator(".cup")
        self.all_coffee_items = self.page.locator("//*[contains(@class, 'cup')]/ancestor::li")
        self.coffee_items_headers = self.all_coffee_items.locator("h4")

    def get_all_coffee_names(self):
        coffee_and_prices = self.coffee_items_headers.all_inner_texts()
        return [coffee.split('\n')[0] for coffee in coffee_and_prices]

    def click_on_nth_cup(self, cup_number):
        self.all_cups.nth(cup_number).click()

    def hover_over_nth_cup(self, cup_number):
        self.all_cups.nth(cup_number).hover()

    def get_coffee_item_by_name(self, coffee_name):
        return [coffee_item for coffee_item in self.all_coffee_items.all() if
                coffee_item.locator("h4").inner_text().split("\n")[0] == coffee_name][0]

    def get_coffee_item_header(self, coffee_name):
        return self.get_coffee_item_by_name(coffee_name).locator("h4")

    def get_coffee_item_ingredients(self, coffee_name):
        return self.get_coffee_item_by_name(coffee_name).locator("[style*='height']")
