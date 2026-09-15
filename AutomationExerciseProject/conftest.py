import logging
import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage
from pages.products_page import ProductsPage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage
from pages.login_page import LoginPage

logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, request):
    """
    Automatically adds a smooth slow-motion delay (800ms) when running in HEADED mode,
    allowing the user to visually analyze and observe the website flow on screen.
    """
    is_headed = False
    if hasattr(request.config.option, "headed"):
        is_headed = bool(request.config.getoption("headed"))
        
    if is_headed:
        return {
            **browser_type_launch_args,
            "slow_mo": 800,  # 800ms delay between every action for clear visual observation
        }
    return browser_type_launch_args

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configures default context options (viewport) for pytest-playwright."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 800},
    }

@pytest.fixture(autouse=True)
def setup_page_and_log_mode(request, page: Page):
    """
    Sets default page timeout and logs clear Browser Mode (HEADED vs HEADLESS).
    """
    is_headed = False
    if hasattr(request.config.option, "headed"):
        is_headed = bool(request.config.getoption("headed"))
        
    browser_mode = "HEADED (Visual Inspection Mode - 800ms SlowMo)" if is_headed else "HEADLESS"
    
    logger.info("-" * 50)
    logger.info(f"Browser Mode: {browser_mode}")
    logger.info("Browser: Chromium")
    logger.info("-" * 50)
    
    page.set_default_timeout(30000)
    yield page

# Page Object Fixtures
@pytest.fixture(scope="function")
def home_page(page: Page) -> HomePage:
    return HomePage(page)

@pytest.fixture(scope="function")
def products_page(page: Page) -> ProductsPage:
    return ProductsPage(page)

@pytest.fixture(scope="function")
def product_detail_page(page: Page) -> ProductDetailPage:
    return ProductDetailPage(page)

@pytest.fixture(scope="function")
def cart_page(page: Page) -> CartPage:
    return CartPage(page)

@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)
