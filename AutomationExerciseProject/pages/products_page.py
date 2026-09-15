from typing import List
from playwright.sync_api import Page, expect

class ProductsPage:
    """
    Page Object for the Products listing page.
    Responsible for category navigation, subcategory selection, and dynamic product listing access.
    """
    
    def __init__(self, page: Page):
        self.page = page
        self.page_header = page.locator(".features_items .title")
        self.category_accordion = page.locator("#accordian")
        self.category_titles = page.locator("#accordian .panel-title a")
        self.product_cards = page.locator(".single-products")
        self.view_product_links = page.locator(".choose a")
        
    def is_loaded(self) -> bool:
        """Verifies that the products page is loaded."""
        expect(self.page_header).to_be_visible()
        return True
        
    def get_available_categories(self) -> List[str]:
        """
        Dynamically gets all available main category names from the sidebar.
        Example: ['Women', 'Men', 'Kids']
        """
        categories = []
        count = self.category_titles.count()
        for i in range(count):
            text = self.category_titles.nth(i).inner_text().strip()
            # Clean text if it has newlines or icons
            clean_name = text.split("\n")[0].strip()
            if clean_name:
                categories.append(clean_name.capitalize())
        return categories
        
    def get_available_subcategories(self, category_name: str) -> List[str]:
        """
        Dynamically gets available subcategories for a given category name.
        """
        formatted_cat = category_name.capitalize()
        # Locator for category expand link (e.g., a[href='#Women'])
        cat_toggle = self.page.locator(f"a[href='#{formatted_cat}']")
        if cat_toggle.is_visible():
            cat_toggle.click()
            self.page.wait_for_timeout(300) # wait for accordion collapse/expand animation
            
        subcat_links = self.page.locator(f"#{formatted_cat} a")
        subcats = []
        count = subcat_links.count()
        for i in range(count):
            subcat_text = subcat_links.nth(i).inner_text().strip()
            if subcat_text:
                subcats.append(subcat_text)
        return subcats
        
    def select_subcategory(self, category_name: str, subcategory_name: str):
        """
        Navigates to a specific subcategory page by clicking the category and subcategory links.
        """
        formatted_cat = category_name.capitalize()
        cat_toggle = self.page.locator(f"a[href='#{formatted_cat}']")
        
        # Ensure category accordion is open
        subcat_container = self.page.locator(f"#{formatted_cat}")
        if not subcat_container.is_visible():
            cat_toggle.click()
            self.page.wait_for_timeout(300)
            
        # Click the subcategory link with exact or matching text
        subcat_link = self.page.locator(f"#{formatted_cat} a", has_text=subcategory_name)
        subcat_link.click()
        self.page.wait_for_url("**/category_products/*", wait_until="domcontentloaded")
        
    def get_product_count(self) -> int:
        """Returns the number of products visible on the page."""
        return self.view_product_links.count()
        
    def open_product_by_index(self, index: int):
        """Opens the product detail page for the product at the specified 0-based index."""
        count = self.view_product_links.count()
        if count == 0:
            raise RuntimeError(f"No products found on page: {self.page.url}")
        if index < 0 or index >= count:
            raise IndexError(f"Product index {index} out of range (0 to {count - 1})")
            
        self.view_product_links.nth(index).click()
        self.page.wait_for_url("**/product_details/*", wait_until="domcontentloaded")
