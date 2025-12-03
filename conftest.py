import pytest
from playwright.sync_api import Page


def pytest_addoption(parser):
    parser.addini("--base-url",
                  help="Base url of the application",
                  default="https://coffee-cart.app/")

def base_url(config):
    cmd_base_url_option = config.getoption("--base-url")
    if cmd_base_url_option is (None or ""):
        return config.getini("--base-url")
    else:
        return cmd_base_url_option

@pytest.fixture
def new_menu_page(request, page: Page):
    page.goto(base_url(request.config))
    return page