from playwright.sync_api import Page, expect

class HomePage:
    """
    Page Object for the Automation Exercise Home Page.
    Handles homepage navigation, header shop-menu controls, and login state checks.
    """
    
    def __init__(self, page: Page):
        self.page = page
        # Locators kept strictly inside the Page Object
        self.logo = page.locator(".logo img")
        self.products_link = page.locator(".shop-menu a[href='/products']")
        self.login_link = page.locator(".shop-menu a[href='/login']")
        self.cart_link = page.locator(".shop-menu a[href='/view_cart']")
        self.logged_in_as_text = page.locator("a:has-text('Logged in as')")
        self.logout_link = page.locator(".shop-menu a[href='/logout']")
        
    def navigate(self):
        """Navigates directly to the homepage."""
        self.page.goto("https://automationexercise.com/", wait_until="domcontentloaded")
        
    def is_loaded(self) -> bool:
        """Verifies that the homepage is loaded by checking logo visibility."""
        expect(self.logo).to_be_visible()
        return True
        
    def go_to_products(self):
        """Navigates to the Products page via top navbar."""
        self.products_link.click()
        self.page.wait_for_url("**/products", wait_until="domcontentloaded")
        
    def go_to_login(self):
        """Navigates to the Login page via top navbar."""
        self.login_link.click()
        self.page.wait_for_url("**/login", wait_until="domcontentloaded")
        
    def go_to_cart(self):
        """Navigates to the Cart page via top navbar."""
        self.cart_link.click()
        self.page.wait_for_url("**/view_cart", wait_until="domcontentloaded")
        
    def is_user_logged_in(self) -> bool:
        """Checks if the user is currently logged in."""
        try:
            expect(self.logged_in_as_text).to_be_visible(timeout=10000)
            return True
        except Exception:
            return False
        
    def get_logged_in_user_name(self) -> str:
        """Gets the username of the logged-in user."""
        expect(self.logged_in_as_text).to_be_visible()
        return self.logged_in_as_text.inner_text().replace("Logged in as", "").strip()
        
    def logout(self):
        """Logs out the user if logged in."""
        if self.logout_link.is_visible():
            self.logout_link.click()
            self.page.wait_for_url("**/login", wait_until="domcontentloaded")
