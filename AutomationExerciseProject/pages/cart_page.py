from typing import Dict, List
from playwright.sync_api import Page, expect

class CartPage:
    """
    Page Object for the Shopping Cart Page.
    Responsible for validating cart contents, product details, prices, and quantities.
    """
    
    def __init__(self, page: Page):
        self.page = page
        self.cart_table = page.locator("#cart_info_table")
        self.cart_rows = page.locator("#cart_info_table tbody tr")
        
    def navigate(self):
        """Navigates directly to the Cart page."""
        self.page.goto("https://automationexercise.com/view_cart", wait_until="domcontentloaded")
        
    def is_loaded(self) -> bool:
        """Verifies that the Cart page is loaded."""
        expect(self.cart_table).to_be_visible()
        return True
        
    def get_cart_items(self) -> List[Dict[str, str]]:
        """
        Retrieves all products currently present in the cart table.
        
        Returns:
            List[Dict]: List of products with keys: name, price, quantity, total.
        """
        expect(self.cart_table).to_be_visible()
        items = []
        count = self.cart_rows.count()
        
        for i in range(count):
            row = self.cart_rows.nth(i)
            name_elem = row.locator(".cart_description h4 a")
            price_elem = row.locator(".cart_price p")
            qty_elem = row.locator(".cart_quantity button")
            total_elem = row.locator(".cart_total p")
            
            if name_elem.is_visible():
                items.append({
                    "name": name_elem.inner_text().strip(),
                    "price": price_elem.inner_text().strip(),
                    "quantity": qty_elem.inner_text().strip(),
                    "total": total_elem.inner_text().strip()
                })
        return items
        
    def get_first_cart_item(self) -> Dict[str, str]:
        """
        Returns details of the first product in the cart.
        Throws RuntimeError if cart is empty.
        """
        items = self.get_cart_items()
        if not items:
            raise RuntimeError(f"Cart is empty on page: {self.page.url}")
        return items[0]
        
    def has_product(self, product_name: str) -> bool:
        """Checks whether a product with the given name exists in the cart."""
        items = self.get_cart_items()
        return any(item["name"].lower() == product_name.lower() for item in items)
