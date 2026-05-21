"""
===============================================================================
LOGIN PAGE OBJECT
===============================================================================

Application:
    OrangeHRM

URL:
    https://opensource-demo.orangehrmlive.com/web/index.php/auth/login

This class follows Page Object Model (POM).

===============================================================================
"""

# Selenium imports
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# Import BasePage class
from pages.base_page import BasePage

# Import config reader
from utils.config_reader import JsonConfigReader


# =============================================================================
# LOAD CONFIGURATION
# =============================================================================

# Read data from config.json
config = JsonConfigReader.load_config()


# =============================================================================
# LOGIN PAGE CLASS
# =============================================================================

class LoginPage(BasePage):

    # Read application URL from config file
    URL = config["base_url"]

    # =========================================================================
    # PAGE LOCATORS
    # =========================================================================


    # Username textbox
    USERNAME_INPUT = (
        By.XPATH,
        "//input[@name='username']"
    )

    # Password textbox
    PASSWORD_INPUT = (
        By.XPATH,
        "//input[@name='password']"
    )

    # Login button
    LOGIN_BTN = (
        By.XPATH,
        "//button[@type='submit']"
    )

    # Error message for invalid login
    ERROR_ALERT = (
        By.XPATH,
        "//p[text()='Invalid credentials'] "
        "| //p[contains(@class, 'oxd-alert-content-text')]"
    )

    # OrangeHRM logo
    BRAND_LOGO = (
        By.XPATH,
        "//div[contains(@class,'orangehrm-login-branding')] "
        "| //img[contains(@alt,'OrangeHRM')]"
    )

    # Dashboard heading after successful login
    DASHBOARD_HEADER = (
        By.XPATH,
        "//h6[normalize-space()='Dashboard']"
    )

    # =========================================================================
    # PAGE ACTION METHODS
    # =========================================================================

    def open_login_page(self):
        """
        Open OrangeHRM login page
        """

        self.log.info("Opening login page")

        # Open application URL
        self.open(self.URL)

        # Wait until username field is visible
        self.wait_for_visible(self.USERNAME_INPUT)

        return self

    def enter_username(self, username):
        """
        Enter username in username field
        """

        self.log.info(f"Entering username: {username}")

        # Type username
        self.type_text(
            self.USERNAME_INPUT,
            username,
            label="Username"
        )

        return self

    def enter_password(self, password):
        """
        Enter password in password field
        """

        self.log.info("Entering password")

        # Type password
        self.type_text(
            self.PASSWORD_INPUT,
            password,
            label="Password"
        )

        return self

    def click_login(self):
        """
        Click Login button
        """

        self.log.info("Clicking Login button")

        # Click login button
        self.click(self.LOGIN_BTN)

    def login(self, username, password):
        """
        Complete login process
        """

        self.log.info("Performing login")

        # Enter username
        self.enter_username(username)

        # Enter password
        self.enter_password(password)

        # Click login button
        self.click_login()

    # =========================================================================
    # VALIDATION METHODS
    # =========================================================================

    def is_login_successful(self):
        """
        Check whether login is successful
        """

        # Wait until URL contains dashboard
        url_changed = self.wait_for_url_contains(
            "dashboard"
        )

        if url_changed:

            self.log.info("Login successful")

            return True

        self.log.warning("Login failed")

        return False

    def is_on_login_page(self):
        """
        Check whether user is still on login page
        """

        # Check login keyword in URL
        result = "login" in self.get_current_url()

        self.log.info(f"Is on login page: {result}")

        return result

    def get_error_message(self):
        """
        Get invalid login error message
        """

        try:
            # Read error text
            message = self.get_text(self.ERROR_ALERT)

            self.log.info(f"Error message: {message}")

            return message

        except TimeoutException:

            self.log.warning("No error message displayed")

            return ""

    def is_brand_logo_displayed(self):
        """
        Check whether OrangeHRM logo is visible
        """

        # Verify logo visibility
        return self.is_displayed(self.BRAND_LOGO)