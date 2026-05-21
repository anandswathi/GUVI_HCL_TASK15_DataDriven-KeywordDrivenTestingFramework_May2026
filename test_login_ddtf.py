"""
===============================================================================
DATA DRIVEN LOGIN TEST
===============================================================================

Framework:
    - Pytest
    - Selenium
    - Page Object Model (POM)
    - Data Driven Testing Framework (DDTF)

Application:
    OrangeHRM

Data Source:
    data/login_test_data.xlsx

Purpose:
    - Read login data from Excel file
    - Execute login test for every row
    - Write PASS / FAIL result back to Excel

===============================================================================
"""

import pytest

# Import Login Page class
from pages.login_page import LoginPage

# Import Excel utility methods
from utils.excel_utils import (
    ExcelUtils,
    RESULT_PASS,
    RESULT_FAIL
)

# Import logger
from utils.logger import get_logger


# =============================================================================
# LOGGER SETUP
# =============================================================================

log = get_logger(__name__)


# =============================================================================
# READ TEST DATA FROM EXCEL
# =============================================================================
# Excel data is loaded once when pytest collects tests


# Read all rows from Excel file
_test_data = ExcelUtils.read_test_data()

# Create test names using test_id
_param_ids = [
    row["test_id"]
    for row in _test_data
]


# =============================================================================
# TEST CLASS
# =============================================================================

class TestLoginDDTF:

    # =========================================================================
    # PARAMETRIZED TEST
    # =========================================================================

    # pytest.mark.parametrize will run test multiple times
    @pytest.mark.parametrize(
        "test_row",
        _test_data,
        ids=_param_ids
    )
    def test_login_with_excel_data(
        self,
        driver,
        test_row
    ):

        """
        Login test using Excel data
        """

        # =====================================================================
        # READ DATA FROM CURRENT EXCEL ROW
        # =====================================================================

        test_id = test_row["test_id"]

        username = test_row["username"]

        password = test_row["password"]

        tester = test_row["tester"]

        row_num = test_row["row"]

        # =====================================================================
        # PRINT TEST DETAILS
        # =====================================================================

        log.info("=" * 70)

        log.info(f"Starting Test : {test_id}")

        log.info(f"Username      : {username}")

        log.info(f"Password      : {'***'}")

        log.info(f"Tester        : {tester}")

        log.info(f"Excel Row     : {row_num}")

        # =====================================================================
        # CREATE LOGIN PAGE OBJECT
        # =====================================================================

        login_page = LoginPage(driver)

        # =====================================================================
        # OPEN LOGIN PAGE
        # =====================================================================

        login_page.open_login_page()

        log.info(
            f"Application Opened : "
            f"{login_page.get_current_url()}"
        )

        # =====================================================================
        # PERFORM LOGIN
        # =====================================================================

        login_page.login(username, password)

        log.info("Login form submitted")

        # =====================================================================
        # CHECK LOGIN RESULT
        # =====================================================================

        # Returns:
        #   True  -> Login successful
        #   False -> Login failed
        login_succeeded = (
            login_page.is_login_successful()
        )

        # =====================================================================
        # WRITE RESULT TO EXCEL
        # =====================================================================

        result = (
            RESULT_PASS
            if login_succeeded
            else RESULT_FAIL
        )

        # Update Excel result column
        ExcelUtils.write_result(
            result,
            row_num
        )

        # =====================================================================
        # PRINT FINAL RESULT
        # =====================================================================

        log.info(f"Test Result   : {result}")

        log.info(
            f"Final URL     : "
            f"{login_page.get_current_url()}"
        )

        log.info("=" * 70)

        # =====================================================================
        # ASSERTION
        # =====================================================================

        # If login fails -> Test will fail in pytest report and Screenshot will be captured automatically
        assert login_succeeded, (

            f"\n{test_id} FAILED"

            f"\nUsername   : {username}"

            f"\nExpected   : Dashboard page"

            f"\nActual URL : "
            f"{login_page.get_current_url()}"

            f"\nExcel Row  : {row_num}"

            f"\nExcel Result Updated : {RESULT_FAIL}"
        )

        # Print success message
        log.info(
            f"{test_id} PASSED - "
            f"Login successful"
        )