import pytest
from playwright.sync_api import expect, Page

from pages.MenuPage import MenuPage
from utils.data_reader_util import read_all_coffee_details_from_file, get_coffee_item_details_by_name

all_coffee_details = read_all_coffee_details_from_file("testdata/coffee_details.json")


@pytest.mark.sanity
@pytest.mark.regression
def test_promo_for_three_different_coffee_items(new_menu_page: Page):
    """ Check adding a discounted coffee from the promo pop up, when 3 different coffee items had been selected."""
    first_cup_number, second_cup_number, third_cup_number = 3, 8, 6
    menu_page = MenuPage(new_menu_page)

    # Add three coffee items to the cart.
    menu_page.click_on_nth_cup(first_cup_number)
    menu_page.click_on_nth_cup(second_cup_number)
    menu_page.click_on_nth_cup(third_cup_number)

    # Check that promo pop up is displayed with correct message.
    discounted_coffee_name = menu_page.get_promo_pop_up_coffee_name()
    discounted_coffee_price = menu_page.get_promo_pop_up_coffee_price()
    expect(menu_page.promo_pop_up).to_be_visible()
    expect(menu_page.promo_message).to_have_text(
        f"It's your lucky day! Get an extra cup of {discounted_coffee_name} for ${discounted_coffee_price}.")

    # Check ingredients of the discounted coffee.
    expected_discounted_coffee_details = get_coffee_item_details_by_name(all_coffee_details, discounted_coffee_name)
    ingredients = menu_page.get_discounted_coffee_item_ingredients()
    expect(ingredients).to_have_count(len(expected_discounted_coffee_details["recipe"]))
    for i, expected_ingredient in enumerate(expected_discounted_coffee_details["recipe"]):
        expected_ingredient_name = expected_ingredient["name"]
        expected_ingredient_quantity = expected_ingredient["quantity"]
        ingredient = ingredients.nth(i)
        expect(ingredient).to_be_visible()
        expect(ingredient).to_have_text(expected_ingredient_name)
        expect(ingredient).to_have_attribute("style", f"height: {expected_ingredient_quantity}%;")

    # Add coffee from the promo pop up.
    menu_page.add_coffee_from_promo_pop_up()

    # Check that promo pop up is gone.
    expect(menu_page.promo_pop_up).not_to_be_visible()

    # Check that cart counter and total value are correct.
    first_coffee_price = menu_page.get_nth_coffee_item_price(first_cup_number)
    second_coffee_price = menu_page.get_nth_coffee_item_price(second_cup_number)
    third_coffee_price = menu_page.get_nth_coffee_item_price(third_cup_number)
    total = first_coffee_price + second_coffee_price + third_coffee_price + discounted_coffee_price
    expect(menu_page.cart_link).to_contain_text("cart (4)")
    expect(menu_page.total_value).to_have_text(f"Total: ${total:.2f}")

    # Check that discounted coffee is in the cart preview.
    menu_page.pay_container.hover()
    expect(menu_page.cart_preview).to_contain_text(f"(Discounted) {discounted_coffee_name} x 1")


@pytest.mark.regression
def test_promo_for_adding_same_coffee_item_thrice(new_menu_page: Page):
    """ Check adding a discounted coffee from the promo pop up, when one coffee item had been selected 3 times."""
    cup_number = 1
    menu_page = MenuPage(new_menu_page)

    # Add one coffee item to the cart three times.
    menu_page.click_on_nth_cup(cup_number)
    menu_page.click_on_nth_cup(cup_number)
    menu_page.click_on_nth_cup(cup_number)

    # Check that promo pop up is displayed with correct message.
    discounted_coffee_name = menu_page.get_promo_pop_up_coffee_name()
    discounted_coffee_price = menu_page.get_promo_pop_up_coffee_price()
    expect(menu_page.promo_pop_up).to_be_visible()
    expect(menu_page.promo_message).to_contain_text(
        f"It's your lucky day! Get an extra cup of {discounted_coffee_name} for ${discounted_coffee_price}.")

    # Add coffee from the promo pop up.
    menu_page.add_coffee_from_promo_pop_up()

    # Check that promo pop up is gone.
    expect(menu_page.promo_pop_up).not_to_be_visible()

    # Check that cart counter and total value are correct.
    coffee_price = menu_page.get_nth_coffee_item_price(cup_number)
    total = 3 * coffee_price + discounted_coffee_price
    expect(menu_page.cart_link).to_contain_text("cart (4)")
    expect(menu_page.total_value).to_have_text(f"Total: ${total:.2f}")

    # Check that discounted coffee is in the cart preview.
    menu_page.pay_container.hover()
    expect(menu_page.cart_preview).to_contain_text(f"(Discounted) {discounted_coffee_name} x 1")


@pytest.mark.regression
def test_refusing_promo(new_menu_page: Page):
    """ Check refusing a discounted coffee from the promo pop up."""
    first_cup_number, second_cup_number, third_cup_number = 0, 3, 2
    menu_page = MenuPage(new_menu_page)

    # Add three coffee items to the cart.
    menu_page.click_on_nth_cup(first_cup_number)
    menu_page.click_on_nth_cup(second_cup_number)
    menu_page.click_on_nth_cup(third_cup_number)

    # Check that promo pop up is displayed.
    expect(menu_page.promo_pop_up).to_be_visible()

    # Refuse coffee from the promo pop up.
    menu_page.refuse_coffee_from_promo_pop_up()

    # Check that promo pop up is gone.
    expect(menu_page.promo_pop_up).not_to_be_visible()

    # Check that cart counter and total value are correct.
    first_coffee_price = menu_page.get_nth_coffee_item_price(first_cup_number)
    second_coffee_price = menu_page.get_nth_coffee_item_price(second_cup_number)
    third_coffee_price = menu_page.get_nth_coffee_item_price(third_cup_number)
    total = first_coffee_price + second_coffee_price + third_coffee_price
    expect(menu_page.cart_link).to_contain_text("cart (3)")
    expect(menu_page.total_value).to_have_text(f"Total: ${total:.2f}")

    # Check that discounted coffee is not in the cart preview.
    menu_page.pay_container.hover()
    expect(menu_page.cart_preview).not_to_contain_text("(Discounted)")


@pytest.mark.regression
def test_ignoring_promo(new_menu_page: Page):
    """ Check ignoring a discounted coffee from the promo pop up."""
    cup_number, additional_cup_number = 4, 2
    menu_page = MenuPage(new_menu_page)

    # Add one coffee item to the cart three times.
    menu_page.click_on_nth_cup(cup_number)
    menu_page.click_on_nth_cup(cup_number)
    menu_page.click_on_nth_cup(cup_number)

    # Check that promo pop up is displayed with correct message.
    expect(menu_page.promo_pop_up).to_be_visible()

    # Ignore promo pop up and choose another coffee item.
    menu_page.click_on_nth_cup(additional_cup_number)

    # Check that promo pop up is gone.
    expect(menu_page.promo_pop_up).not_to_be_visible()

    # Check that cart counter and total value are correct.
    coffee_price = menu_page.get_nth_coffee_item_price(cup_number)
    additional_coffee_price = menu_page.get_nth_coffee_item_price(additional_cup_number)
    total = 3 * coffee_price + additional_coffee_price
    expect(menu_page.cart_link).to_contain_text("cart (4")
    expect(menu_page.total_value).to_have_text(f"Total: ${total:.2f}")

    # Check that discounted coffee is not in the cart preview.
    menu_page.pay_container.hover()
    expect(menu_page.cart_preview).not_to_contain_text("(Discounted)")


@pytest.mark.regression
def test_promo_shows_multiple_times(new_menu_page: Page):
    """ Check that promo is shown every time three coffee items are selected."""
    cup_number, additional_cup_number = 4, 2
    menu_page = MenuPage(new_menu_page)

    # Add one coffee item to the cart three times.
    menu_page.click_on_nth_cup(cup_number)
    menu_page.click_on_nth_cup(cup_number)
    menu_page.click_on_nth_cup(cup_number)

    # Check that promo pop up is displayed.
    first_discounted_coffee_name = menu_page.get_promo_pop_up_coffee_name()
    first_discounted_coffee_price = menu_page.get_promo_pop_up_coffee_price()
    expect(menu_page.promo_pop_up).to_be_visible()

    # Add coffee from the promo pop up.
    menu_page.add_coffee_from_promo_pop_up()

    # Check that promo pop up is gone.
    expect(menu_page.promo_pop_up).not_to_be_visible()

    # Add additional coffee item to the cart two times, which amounts to three more coffee items in total.
    menu_page.click_on_nth_cup(additional_cup_number)
    menu_page.click_on_nth_cup(additional_cup_number)

    # Check that promo pop up is displayed.
    second_discounted_coffee_name = menu_page.get_promo_pop_up_coffee_name()
    second_discounted_coffee_price = menu_page.get_promo_pop_up_coffee_price()
    expect(menu_page.promo_pop_up).to_be_visible()

    # Add coffee from the promo pop up once again.
    menu_page.add_coffee_from_promo_pop_up()

    # Check that promo pop up is gone.
    expect(menu_page.promo_pop_up).not_to_be_visible()

    # Check that cart counter and total value are correct.
    coffee_price = menu_page.get_nth_coffee_item_price(cup_number)
    additional_coffee_price = menu_page.get_nth_coffee_item_price(additional_cup_number)
    total = (3 * coffee_price + 2 * additional_coffee_price +
             first_discounted_coffee_price + second_discounted_coffee_price)
    expect(menu_page.cart_link).to_contain_text("cart (7)")
    expect(menu_page.total_value).to_have_text(f"Total: ${total:.2f}")

    # Check that discounted coffee is in the cart preview.
    menu_page.pay_container.hover()
    if first_discounted_coffee_name == second_discounted_coffee_name:
        expect(menu_page.cart_preview).to_contain_text(f"(Discounted) {first_discounted_coffee_name} x 2")
    else:
        expect(menu_page.cart_preview).to_contain_text(f"(Discounted) {first_discounted_coffee_name} x 1")
        expect(menu_page.cart_preview).to_contain_text(f"(Discounted) {second_discounted_coffee_name} x 1")
