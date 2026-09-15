from typing import Dict
from playwright.sync_api import Page, expect

class ProductDetailPage:
    """
    Page Object for the Product Detail Page.
    Responsible for capturing product specifications and adding the product to the cart.
    """
    
    def __init__(self, page: Page):
        self.page = page
        self.product_name = page.locator(".product-information h2")
        self.product_price = page.locator(".product-information span span")
        self.product_category = page.locator(".product-information p:has-text('Category:')")
        self.product_availability = page.locator(".product-information p:has-text('Availability:')")
        self.product_condition = page.locator(".product-information p:has-text('Condition:')")
        self.product_brand = page.locator(".product-information p:has-text('Brand:')")
        self.add_to_cart_button = page.locator("button.cart")
        self.view_cart_modal_link = page.locator("#cartModal a[href='/view_cart']")
        
    def is_loaded(self) -> bool:
        """Verifies that the product detail page is loaded."""
        expect(self.product_name).to_be_visible()
        return True
        
    def get_product_details(self) -> Dict[str, str]:
        """
        Captures dynamic details of the selected product.
        
        Returns:
            Dict containing name, price, category, availability, condition, brand.
        """
        expect(self.product_name).to_be_visible()
        
        name = self.product_name.inner_text().strip()
        price = self.product_price.inner_text().strip()
        category = self.product_category.inner_text().replace("Category:", "").strip() if self.product_category.is_visible() else "N/A"
        availability = self.product_availability.inner_text().replace("Availability:", "").strip() if self.product_availability.is_visible() else "N/A"
        condition = self.product_condition.inner_text().replace("Condition:", "").strip() if self.product_condition.is_visible() else "N/A"
        brand = self.product_brand.inner_text().replace("Brand:", "").strip() if self.product_brand.is_visible() else "N/A"
        
        return {
            "name": name,
            "price": price,
            "category": category,
            "availability": availability,
            "condition": condition,
            "brand": brand
        }
        
    def add_to_cart(self):
        """Clicks the Add to cart button."""
        expect(self.add_to_cart_button).to_be_visible()
        self.add_to_cart_button.click()
        
    def proceed_to_cart(self):
        """Clicks View Cart in the confirmation modal."""
        expect(self.view_cart_modal_link).to_be_visible()
        self.view_cart_modal_link.click()
        self.page.wait_for_url("**/view_cart", wait_until="domcontentloaded")
