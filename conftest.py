import pytest
from playwright.sync_api import Page

@pytest.fixture
def new_menu_page(page: Page):
    page.goto("https://coffee-cart.app/")
    return page