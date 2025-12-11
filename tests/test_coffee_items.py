import re

import pytest
from playwright.sync_api import Page, expect
from pages.MenuPage import MenuPage
from utils.data_reader_util import read_all_coffee_details_from_file, get_coffee_item_details_by_name


@pytest.mark.sanity
@pytest.mark.regression
def test_no_duplicates_in_coffee_names(new_menu_page: Page):
    """Checks that the coffee names are unique"""
    menu_page = MenuPage(new_menu_page)
    coffee_names = menu_page.get_all_coffee_names()

    # Check that the list of coffee names does not contain duplicates.
    assert len(coffee_names) == len(set(coffee_names))


@pytest.mark.sanity
@pytest.mark.regression
@pytest.mark.dependency(depends=["test_no_duplicates_in_cups_names"])
def test_coffee_details(new_menu_page: Page):
    """Check coffee details for each item on the menu page,
    assuming that there are no duplicate coffee names on the menu page.
    """
    menu_page = MenuPage(new_menu_page)
    all_coffee_details = read_all_coffee_details_from_file("testdata/coffee_details.json")

    for coffee_name in menu_page.get_all_coffee_names():
        expected_coffee_details = get_coffee_item_details_by_name(all_coffee_details, coffee_name)
        coffee_item_header = menu_page.get_coffee_item_header(coffee_name)

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
    cup_number = 0
    menu_page = MenuPage(new_menu_page)
    cup = menu_page.all_cups.nth(cup_number)
    expect(cup).to_have_css("transform", "none")
    menu_page.hover_over_nth_cup(cup_number)
    expect(cup).to_have_css("cursor", "pointer")
    expect(cup).to_have_css("transform", re.compile("^matrix*"))
