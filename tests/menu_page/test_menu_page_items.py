import re
import pytest
from playwright.sync_api import Page, expect
from pages.MenuPage import MenuPage
from utils.data_reader_util import read_all_coffee_details_from_file

all_coffee_details = read_all_coffee_details_from_file("testdata/coffee_details.json")


@pytest.mark.regression
def test_url_and_title(base_url, new_menu_page: Page):
    """Check url and title of the menu page."""
    expect(new_menu_page).to_have_url(base_url)
    expect(new_menu_page).to_have_title("Coffee cart")


@pytest.mark.regression
def test_default_cart_counter_and_total(new_menu_page: Page):
    """Check that default values of cart counter and 'Total' are zero."""
    menu_page = MenuPage(new_menu_page)
    expect(menu_page.cart_link).to_have_text("cart (0)")
    expect(menu_page.total_value).to_have_text("Total: $0.00")


@pytest.mark.sanity
@pytest.mark.regression
def test_no_duplicates_in_coffee_names(new_menu_page: Page):
    """Checks that the coffee names are unique"""
    menu_page = MenuPage(new_menu_page)
    coffee_names = menu_page.get_all_coffee_names()
    assert len(coffee_names) == len(set(coffee_names)), \
        "Duplicate coffee names found on the menu page."


@pytest.mark.sanity
@pytest.mark.regression
@pytest.mark.dependency(depends=["test_no_duplicates_in_cups_names"])
@pytest.mark.parametrize('expected_coffee_details', [coffee_details for coffee_details
                                                     in all_coffee_details
                                                     if not "(Discounted)" in coffee_details["name"]])
def test_coffee_details(expected_coffee_details, new_menu_page: Page):
    """Check coffee details for each item on the menu page,
    assuming that there are no duplicate coffee names on the menu page.
    """
    menu_page = MenuPage(new_menu_page)
    coffee_name = expected_coffee_details["name"]
    coffee_item_header = menu_page.get_coffee_item_header_by_name(coffee_name)

    # Check that coffee name and price are correct.
    expect(coffee_item_header).to_have_text(
        f"{expected_coffee_details["name"]} ${expected_coffee_details['price']:.2f}")

    # Check that ingredients count is correct.
    ingredients = menu_page.get_coffee_item_ingredients(coffee_name)
    expect(ingredients).to_have_count(len(expected_coffee_details["recipe"]))

    # Check each ingredient's name and quantity.
    for i, expected_ingredient in enumerate(expected_coffee_details["recipe"]):
        expected_ingredient_name = expected_ingredient["name"]
        expected_ingredient_quantity = expected_ingredient["quantity"]
        ingredient = ingredients.nth(i)
        expect(ingredient).to_be_visible()
        expect(ingredient).to_have_text(expected_ingredient_name)
        expect(ingredient).to_have_attribute("style", f"height: {expected_ingredient_quantity}%;")


@pytest.mark.regression
def test_hover_state(new_menu_page: Page):
    """Check that a cup is rotated on hover."""
    cup_number = 3
    menu_page = MenuPage(new_menu_page)
    cup = menu_page.all_cups.nth(cup_number)
    expect(cup).to_have_css("transform", "none")
    menu_page.hover_over_nth_cup(cup_number)
    expect(cup).to_have_css("cursor", "pointer")
    expect(cup).to_have_css("transform", re.compile("^matrix*"))


@pytest.mark.regression
@pytest.mark.parametrize('coffee_details', [coffee_details for coffee_details
                                            in all_coffee_details
                                            if not "(Discounted)" in coffee_details["name"]])
def test_chinese_coffee_name(coffee_details, new_menu_page: Page):
    """Check that coffee name is shown in Chinese on double click."""
    coffee_name = coffee_details["name"]
    coffee_name_chinese = coffee_details["name_chinese"]
    menu_page = MenuPage(new_menu_page)
    menu_page.double_click_coffee_header_by_name(coffee_name)
    coffee_header = menu_page.get_coffee_item_header_by_name(coffee_name_chinese)
    expect(coffee_header).to_be_visible()
