import pytest
from playwright.sync_api import Page


def pytest_addoption(parser):
    parser.addini("--base-url",
                  help="Base url of the application",
                  default="https://coffee-cart.app/")


def base_url(config):
    return config.getoption("--base-url") or config.getini("--base-url")


@pytest.fixture
def new_menu_page(request, page: Page):
    page.goto(base_url(request.config))
    yield page
