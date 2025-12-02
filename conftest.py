import pytest
from playwright.sync_api import Page


def pytest_addoption(parser):
    parser.addini("--base-url",
                  help="Base url of the application",
                  default="https://coffee-cart.app/")

@pytest.fixture
def new_menu_page(request, page: Page):
    cmd_base_url_option = request.config.getoption("--base-url")
    if cmd_base_url_option is (None or ""):
        page.goto(request.config.getini("--base-url"))
    else:
        page.goto(cmd_base_url_option)
    return page