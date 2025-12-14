from playwright.sync_api import Page


class MenuPage:

    def __init__(self, page: Page):
        self.page = page

        self.cart_link = self.page.locator('a[href="/cart"]')
        self.all_cups = self.page.locator(".cup")
        self.all_coffee_items = self.page.locator("//*[contains(@class, 'cup')]/ancestor::li")
        self.coffee_items_headers = self.all_coffee_items.locator("h4")
        self.total_value = self.page.locator(".pay")
        self.pay_container = self.page.locator(".pay-container")
        self.cart_preview = self.page.locator(".cart-preview")
        self.add_coffee_to_cart_question = self.page.locator("dialog p")
        self.yes_to_add_to_cart = self.page.locator('button:has-text("Yes")')
        self.no_to_add_to_cart = self.page.locator('button:has-text("No")')
        self.promo_pop_up = self.page.locator(".promo")
        self.promo_message = self.promo_pop_up.locator("span")
        self.yes_to_add_promo_to_cart = self.promo_pop_up.locator("button:has-text(\"Yes, of course!\")")
        self.no_to_add_promo_to_cart = self.promo_pop_up.locator("button:has-text(\"Nah, I'll skip.\")")
        self.checkout_modal_window = self.page.locator(".modal")
        self.checkout_name = self.checkout_modal_window.get_by_label("Name")
        self.checkout_email = self.checkout_modal_window.get_by_label("Email")
        self.checkout_promotion_agreement = self.checkout_modal_window.locator("#promotion")
        self.submit_order_button = self.checkout_modal_window.locator("#submit-payment")
        self.successful_checkout_message = self.page.locator(".snackbar")
        self.close_checkout_dialog_button = self.page.locator(".close")

    def get_all_coffee_names(self):
        coffee_and_prices = self.coffee_items_headers.all_inner_texts()
        return [coffee.split('\n')[0] for coffee in coffee_and_prices]

    def click_on_nth_cup(self, cup_number):
        self.all_cups.nth(cup_number).click()

    def right_click_on_nth_cup(self, cup_number):
        self.all_cups.nth(cup_number).click(button="right")

    def agree_to_add_to_cart(self):
        self.yes_to_add_to_cart.click()

    def refuse_to_add_to_cart(self):
        self.no_to_add_to_cart.click()

    def hover_over_nth_cup(self, cup_number):
        self.all_cups.nth(cup_number).hover()

    def get_nth_coffee_item_name(self, cup_number):
        return self.coffee_items_headers.nth(cup_number).inner_text().split("\n")[0]

    def get_nth_coffee_item_price(self, cup_number):
        return float(self.coffee_items_headers.nth(cup_number).inner_text().split("\n")[1].split("$")[1])

    def get_coffee_item_by_name(self, coffee_name):
        return self.page.locator(f"//h4[text() = '{coffee_name} ']/parent::li")

    def get_coffee_item_header_by_name(self, coffee_name):
        return self.get_coffee_item_by_name(coffee_name).locator("h4")

    def double_click_coffee_header_by_name(self, coffee_name):
        self.get_coffee_item_header_by_name(coffee_name).dblclick()

    def get_coffee_item_ingredients(self, coffee_name):
        return self.get_coffee_item_by_name(coffee_name).locator("[style*='height']")

    def get_discounted_coffee_item_ingredients(self):
        return self.promo_pop_up.locator("[style*='height']")

    def add_from_cart_preview_by_name(self, coffee_name):
        self.cart_preview.locator(f"//span[text()='{coffee_name}']/ancestor::li//button[text()='+']").click()

    def remove_from_cart_preview_by_name(self, coffee_name):
        self.cart_preview.locator(f"//span[text()='{coffee_name}']/ancestor::li//button[text()='-']").click()

    def get_coffee_names_in_cart_preview(self):
        return [
            item.inner_text().split(" x ")[0]
            for item in self.cart_preview.locator("li").all()
        ]

    def get_promo_pop_up_coffee_name(self):
        return self.promo_message.inner_text().split("It's your lucky day! Get an extra cup of ")[1].split(" for $")[0]

    def get_promo_pop_up_coffee_price(self):
        return int(self.promo_message.inner_text().split(
            "It's your lucky day! Get an extra cup of ")[1].split(" for $")[1].rstrip("."))

    def add_coffee_from_promo_pop_up(self):
        self.yes_to_add_promo_to_cart.click()

    def refuse_coffee_from_promo_pop_up(self):
        self.no_to_add_promo_to_cart.click()
