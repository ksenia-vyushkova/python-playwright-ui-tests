import pytest
from playwright.sync_api import Page, expect
from pages.MenuPage import MenuPage
from utils.data_reader_util import read_json_coffee_item_data_by_name


@pytest.mark.regression
def test_no_duplicates_in_coffee_names(new_menu_page: Page):
    """ Checks that the coffee names are unique"""
    menu_page = MenuPage(new_menu_page)
    coffee_names = menu_page.get_coffee_names()

    # Check that the list of coffee names does not contain duplicates.
    assert len(coffee_names) == len(set(coffee_names))


@pytest.mark.regression
@pytest.mark.dependency(depends=["test_no_duplicates_in_cups_names"])
def test_coffee_names_and_prices(new_menu_page: Page):
    """ Check coffee details for each item on the menu page.
        Assume that there are no duplicate coffee names on the menu page.
    """
    menu_page = MenuPage(new_menu_page)
    for coffee_name in menu_page.get_coffee_names():
        expected_coffee_item = read_json_coffee_item_data_by_name(
            "testdata/coffee_details.json", coffee_name)
        actual_coffee_item = menu_page.find_coffee_item_by_name(coffee_name)
        # Check that coffee name and price are correct.
        expect(actual_coffee_item.locator("h4")).to_have_text(
            expected_coffee_item["name"] + " $" + f"{expected_coffee_item['price']:.2f}")
