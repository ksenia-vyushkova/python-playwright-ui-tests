import pytest
from playwright.sync_api import Page


@pytest.fixture
def new_menu_page(page: Page):
    """ Navigate to base url."""
    page.goto("/")
    yield page
