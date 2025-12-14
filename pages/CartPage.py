from playwright.sync_api import Page


class CartPage:

    def __init__(self, page: Page):
        self.page = page

        self.cart_link = self.page.locator('a[href="/cart"]')
        self.cart_list = self.page.locator(".list")
        self.total_value = self.page.locator(".pay")
        self.list_header_1 = self.page.locator(".list-header *:nth-child(1)")
        self.list_header_2 = self.page.locator(".list-header *:nth-child(2)")
        self.list_header_3 = self.page.locator(".list-header *:nth-child(3)")

    def delete_coffee_from_cart_by_name(self, coffee_name):
        self.page.locator(
            f"//*[@class ='list']/div/ul/li[descendant::*[text() = '{coffee_name}']]//button[@class = 'delete']").click()

    def get_list_entry_for_coffee(self, coffee_name):
        return self.page.locator(
            f"//*[@class ='list']/div/ul/li[descendant::*[text() = '{coffee_name}']]")

    def get_row_text(self, coffee_name, coffee_price, coffee_quantity):
        return f"{coffee_name}${coffee_price:.2f} x {coffee_quantity}+-${coffee_price * coffee_quantity:.2f}x"

    def get_coffee_names_in_cart(self):
        return [
            item.inner_text()
            for item in self.page.locator(
                "//*[@class ='list']/div/ul/li[@class = 'list-item']/div[1]").all()
        ]
