import os
import logging
import pytest
from utils.csv_reader import read_login_data_csv

logger = logging.getLogger(__name__)

# Load login data dynamically from CSV
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "test_data", "login_data.csv")
LOGIN_TEST_DATA = read_login_data_csv(os.path.abspath(CSV_PATH))

@pytest.mark.parametrize("account_data", LOGIN_TEST_DATA, ids=[row["email"] + "-" + row["expected_result"] for row in LOGIN_TEST_DATA])
def test_login_data_driven(login_page, home_page, account_data):

    email = account_data["email"]
    password = account_data["password"]
    expected_result = account_data["expected_result"].lower()
    
    logger.info("=" * 60)
    logger.info(f"STARTING DATA-DRIVEN LOGIN TEST FOR ACCOUNT: {email}")
    logger.info(f"Expected Result: {expected_result.upper()}")
    logger.info("=" * 60)
    
    # 1. Open login page
    login_page.navigate()
    assert login_page.is_loaded(), "Login page failed to load."
    
    # 2. Submit login form
    logger.info(f"Submitting credentials for '{email}'")
    login_page.login(email, password)
    
    # 3. Validate based on expected result
    if expected_result == "success":
        # Assert login succeeded
        assert home_page.is_user_logged_in(), f"Expected successful login for '{email}', but user is not logged in."
        logged_user = home_page.get_logged_in_user_name()
        logger.info(f"ACTUAL RESULT: SUCCESS | Logged in user: '{logged_user}'")
        
        # Cleanup state for next test iteration
        logger.info("Cleaning up session state by logging out...")
        home_page.logout()
        
    elif expected_result == "failure":
        # Assert login failed and error message displayed
        assert login_page.is_error_displayed(), f"Expected error message for failed login of '{email}', but no error was displayed."
        error_msg = login_page.get_error_message()
        assert not home_page.is_user_logged_in(), f"Expected user '{email}' to remain logged out, but user is logged in."
        logger.info(f"ACTUAL RESULT: FAILURE | Error Message Displayed: '{error_msg}'")
        
    else:
        pytest.fail(f"Invalid expected_result value in CSV: '{expected_result}'. Expected 'success' or 'failure'.")
        
    logger.info(f"PASSED Data-Driven Login Test for '{email}' [{expected_result}]")
    logger.info("=" * 60)
