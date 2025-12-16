# python-playwright-ui-tests

This project consists of UI tests for a Coffee Cart demo application at https://coffee-cart.app/.

The following Windows batch command may be used to run the tests:

```
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
playwright install
pytest -m "regression"
```
