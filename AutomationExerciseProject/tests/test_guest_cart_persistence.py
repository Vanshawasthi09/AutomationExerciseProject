import os
import random
import logging

logger = logging.getLogger(__name__)

def test_guest_cart_persistence_after_login(home_page, products_page, product_detail_page, cart_page, login_page):
    """
    TEST CASE 1 — FULL END-TO-END TEST: Guest Cart Persistence After Login.
    
    Verifies that a product dynamically selected and added to the cart as a guest 
    remains preserved in the cart after the user authenticates.
    """
    # 1. Randomization setup (reproducible seed)
    seed_env = os.getenv("TEST_SEED")
    seed = int(seed_env) if seed_env and seed_env.isdigit() else random.randint(100000, 999999)
    rng = random.Random(seed)
    
    logger.info("=" * 60)
    logger.info("STARTING TEST CASE 1: Guest Cart Persistence After Login")
    logger.info(f"Random Seed: {seed}")
    logger.info("=" * 60)
    
    # 2. Open Homepage and verify
    logger.info("Step 1: Opening Automation Exercise Homepage")
    home_page.navigate()
    assert home_page.is_loaded(), "Homepage failed to load properly."
    
    # 3. Navigate to Products page
    logger.info("Step 2: Navigating to Products Page")
    home_page.go_to_products()
    assert products_page.is_loaded(), "Products Page failed to load properly."
    
    # 4. Dynamically identify and randomly select main Category
    categories = products_page.get_available_categories()
    logger.info(f"Available Categories: {categories}")
    assert len(categories) > 0, "No categories found on Products page."
    selected_category = rng.choice(categories)
    logger.info(f"Randomly Selected Category: {selected_category}")
    
    # 5. Dynamically identify and randomly select Subcategory
    subcategories = products_page.get_available_subcategories(selected_category)
    logger.info(f"Available Subcategories for '{selected_category}': {subcategories}")
    assert len(subcategories) > 0, f"No subcategories found for category '{selected_category}'."
    selected_subcategory = rng.choice(subcategories)
    logger.info(f"Randomly Selected Subcategory: {selected_subcategory}")
    
    # 6. Open selected subcategory page
    logger.info(f"Step 3: Opening Subcategory '{selected_subcategory}'")
    products_page.select_subcategory(selected_category, selected_subcategory)
    
    # 7. Dynamically collect available products and randomly select one
    product_count = products_page.get_product_count()
    logger.info(f"Total products available in '{selected_subcategory}': {product_count}")
    assert product_count > 0, f"No products found for subcategory '{selected_subcategory}'."
    
    selected_index = rng.randint(0, product_count - 1)
    logger.info(f"Randomly Selected Product Index: {selected_index} (out of {product_count})")
    products_page.open_product_by_index(selected_index)
    
    # 8. Verify product detail page and capture details
    assert product_detail_page.is_loaded(), "Product Detail Page failed to load."
    product_details = product_detail_page.get_product_details()
    
    selected_product_name = product_details["name"]
    selected_product_price = product_details["price"]
    selected_product_category = product_details["category"]
    
    logger.info("-" * 40)
    logger.info(f"CAPTURED PRODUCT DETAILS:")
    logger.info(f"Product Name:     {selected_product_name}")
    logger.info(f"Product Price:    {selected_product_price}")
    logger.info(f"Product Category: {selected_product_category}")
    logger.info("-" * 40)
    
    # 9. Add product to cart as guest and open Cart
    logger.info("Step 4: Adding product to cart as Guest")
    product_detail_page.add_to_cart()
    product_detail_page.proceed_to_cart()
    
    assert cart_page.is_loaded(), "Cart Page failed to load after adding item."
    assert cart_page.has_product(selected_product_name), f"Product '{selected_product_name}' missing from Guest Cart."
    
    # Find matching guest item in cart
    guest_cart_items = cart_page.get_cart_items()
    guest_cart_item = next((item for item in guest_cart_items if item["name"] == selected_product_name), None)
    assert guest_cart_item is not None, f"Failed to retrieve baseline details for '{selected_product_name}' from guest cart."
    
    logger.info("-" * 40)
    logger.info(f"GUEST CART BASELINE DATA:")
    logger.info(f"Guest Item Name:  {guest_cart_item['name']}")
    logger.info(f"Guest Item Price: {guest_cart_item['price']}")
    logger.info(f"Guest Quantity:   {guest_cart_item['quantity']}")
    logger.info(f"Guest Total:      {guest_cart_item['total']}")
    logger.info("-" * 40)
    
    # 10. Navigate to Login page and authenticate
    logger.info("Step 5: Navigating to Login Page and Authenticating")
    home_page.go_to_login()
    assert login_page.is_loaded(), "Login Page failed to load."
    
    # Create or use isolated account credentials
    valid_email = f"user_seed_{seed}@example.com"
    valid_password = "TestPassword123"
    
    # Register pristine user account dynamically for seed isolation
    page = home_page.page
    page.locator("input[data-qa='signup-name']").fill("Test User")
    page.locator("input[data-qa='signup-email']").fill(valid_email)
    page.locator("button[data-qa='signup-button']").click()
    
    # Fill registration details
    page.locator("#id_gender1").check()
    page.locator("#password").fill(valid_password)
    page.locator("#days").select_option("1")
    page.locator("#months").select_option("January")
    page.locator("#years").select_option("2000")
    page.locator("#first_name").fill("Test")
    page.locator("#last_name").fill("User")
    page.locator("#address1").fill("123 Test St")
    page.locator("#country").select_option("United States")
    page.locator("#state").fill("CA")
    page.locator("#city").fill("Los Angeles")
    page.locator("#zipcode").fill("90001")
    page.locator("#mobile_number").fill("1234567890")
    page.locator("button[data-qa='create-account']").click()
    page.locator("a[data-qa='continue-button']").click()
    
    # Verify user is logged in
    assert home_page.is_user_logged_in(), f"User login failed for {valid_email}."
    logged_user = home_page.get_logged_in_user_name()
    logger.info(f"Login Successful! Logged in as: '{logged_user}' ({valid_email})")
    
    # 11. Open Cart after login and verify persistence
    logger.info("Step 6: Re-opening Cart as Logged-in User")
    home_page.go_to_cart()
    assert cart_page.is_loaded(), "Cart Page failed to load for logged-in user."
    assert cart_page.has_product(selected_product_name), f"Cart persistence failed! Expected product '{selected_product_name}' not found."
    
    # Find matching logged-in item in cart
    loggedin_cart_items = cart_page.get_cart_items()
    loggedin_cart_item = next((item for item in loggedin_cart_items if item["name"] == selected_product_name), None)
    assert loggedin_cart_item is not None, f"Failed to retrieve details for '{selected_product_name}' from logged-in cart."
    
    logger.info("-" * 40)
    logger.info(f"LOGGED-IN CART DATA:")
    logger.info(f"Logged-in Item Name:  {loggedin_cart_item['name']}")
    logger.info(f"Logged-in Item Price: {loggedin_cart_item['price']}")
    logger.info(f"Logged-in Quantity:   {loggedin_cart_item['quantity']}")
    logger.info(f"Logged-in Total:      {loggedin_cart_item['total']}")
    logger.info("-" * 40)
    
    # 12. Assertions & Comparisons
    logger.info("Step 7: Validating Cart State Preservation")
    assert guest_cart_item["name"] == loggedin_cart_item["name"], \
        f"Product Name mismatch! Guest: '{guest_cart_item['name']}', Logged-in: '{loggedin_cart_item['name']}'"
    assert guest_cart_item["price"] == loggedin_cart_item["price"], \
        f"Product Price mismatch! Guest: '{guest_cart_item['price']}', Logged-in: '{loggedin_cart_item['price']}'"
    assert guest_cart_item["quantity"] == loggedin_cart_item["quantity"], \
        f"Product Quantity mismatch! Guest: '{guest_cart_item['quantity']}', Logged-in: '{loggedin_cart_item['quantity']}'"
        
    logger.info("SUCCESS: Cart persistence after login verified successfully!")
    logger.info("=" * 60)
