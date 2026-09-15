from playwright.sync_api import Page, expect

class LoginPage:
    """
    Page Object for the Login/Signup Page.
    Responsible for handling user authentication and validating login results.
    """
    
    def __init__(self, page: Page):
        self.page = page
        self.login_form = page.locator(".login-form")
        self.email_input = page.locator("input[data-qa='login-email']")
        self.password_input = page.locator("input[data-qa='login-password']")
        self.login_button = page.locator("button[data-qa='login-button']")
        self.error_message = page.locator(".login-form p")
        
    def navigate(self):
        """Navigates directly to the Login page."""
        self.page.goto("https://automationexercise.com/login", wait_until="domcontentloaded")
        
    def is_loaded(self) -> bool:
        """Verifies that the Login page is loaded."""
        expect(self.login_form).to_be_visible()
        return True
        
    def login(self, email: str, password: str):
        """
        Enters email and password, then submits the login form.
        """
        expect(self.email_input).to_be_visible()
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
        
    def get_error_message(self) -> str:
        """Returns the text of the login error message if displayed."""
        if self.error_message.is_visible():
            return self.error_message.inner_text().strip()
        return ""
        
    def is_error_displayed(self) -> bool:
        """Checks if an error message is visible on login failure with auto-wait."""
        try:
            expect(self.error_message).to_be_visible(timeout=10000)
            return True
        except Exception:
            return False
