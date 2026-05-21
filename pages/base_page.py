"""
===============================================================================
Base Page Class
===============================================================================

 -> This is the parent class for all Page Objects.

 -> All page classes will inherit this BasePage class.

===============================================================================
"""

# Selenium wait classes
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Selenium exceptions
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
)

# Custom utility files
from utils.config_reader import JsonConfigReader
from utils.logger import get_logger


# =============================================================================
# LOAD CONFIGURATION
# =============================================================================

# Read values from config.json
config = JsonConfigReader.load_config()


# =============================================================================
# BASE PAGE CLASS
# =============================================================================

class BasePage:

    # Read timeout value from config file
    TIMEOUT = config["timeout"]

    # =========================================================================
    # CONSTRUCTOR
    # =========================================================================

    # This method runs automatically when object is created
    def __init__(self, driver):

        # Store driver object
        self.driver = driver

        # Create explicit wait object
        self.wait = WebDriverWait(driver, self.TIMEOUT)

        # Create logger object
        self.log = get_logger(self.__class__.__module__)

    # =========================================================================
    # PAGE NAVIGATION METHODS
    # =========================================================================

    def open(self, url: str) -> None:
        """
        Open application URL
        """

        self.log.info(f"Opening URL: {url}")

        # Open webpage
        self.driver.get(url)

    def get_current_url(self) -> str:
        """
        Return current page URL
        """

        # Get current URL
        url = self.driver.current_url

        self.log.info(f"Current URL: {url}")

        return url

    def get_title(self) -> str:
        """
        Return page title
        """

        # Get page title
        title = self.driver.title

        self.log.info(f"Page Title: {title}")

        return title

    # =========================================================================
    # WAIT METHODS
    # =========================================================================

    # These methods use Explicit Wait
    def wait_for_visible(self, locator: tuple):
        """
        Wait until element becomes visible
        """

        self.log.info(f"Waiting for visible element: {locator}")

        try:
            # Wait for element visibility
            element = self.wait.until(
                EC.visibility_of_element_located(locator)
            )

            return element

        except TimeoutException:

            self.log.error(
                f"Element not visible after {self.TIMEOUT} seconds"
            )

            raise

    def wait_for_clickable(self, locator: tuple):
        """
        Wait until element becomes clickable
        """

        self.log.info(f"Waiting for clickable element: {locator}")

        try:
            # Wait for clickable element
            element = self.wait.until(
                EC.element_to_be_clickable(locator)
            )

            return element

        except TimeoutException:

            self.log.error(
                f"Element not clickable after {self.TIMEOUT} seconds"
            )

            raise

    def wait_for_present(self, locator: tuple):
        """
        Wait until element is present in DOM
        """

        self.log.info(f"Waiting for element presence: {locator}")

        try:
            # Wait until element exists
            element = self.wait.until(
                EC.presence_of_element_located(locator)
            )

            return element

        except TimeoutException:

            self.log.error(
                f"Element not present after {self.TIMEOUT} seconds"
            )

            raise

    def wait_for_url_contains(self, text: str) -> bool:
        """
        Wait until URL contains given text
        """

        self.log.info(f"Waiting for URL to contain: {text}")

        try:
            # Wait until URL contains text
            return self.wait.until(
                EC.url_contains(text)
            )

        except TimeoutException:

            self.log.warning(
                f"URL does not contain '{text}'"
            )

            return False

    def wait_for_text_in_element(
        self,
        locator: tuple,
        text: str
    ) -> bool:
        """
        Wait until element contains text
        """

        self.log.info(
            f"Waiting for text '{text}' inside element"
        )

        try:
            # Wait until text appears
            return self.wait.until(
                EC.text_to_be_present_in_element(locator, text)
            )

        except TimeoutException:

            self.log.warning(
                f"Text '{text}' not found"
            )

            return False

    # =========================================================================
    # ELEMENT ACTION METHODS
    # =========================================================================

    def click(self, locator: tuple) -> None:
        """
        Click on element
        """

        self.log.info(f"Clicking element: {locator}")

        try:
            # Wait and click element
            self.wait_for_clickable(locator).click()

        except ElementNotInteractableException:

            # Use JavaScript click if normal click fails
            self.log.warning(
                "Normal click failed. Using JavaScript click."
            )

            self.driver.execute_script(
                "arguments[0].click();",
                self.wait_for_present(locator)
            )

    def type_text(
        self,
        locator: tuple,
        text: str,
        label: str = ""
    ) -> None:
        """
        Enter text inside input field
        """

        # Hide password in logs
        masked_text = (
            "***"
            if "password" in label.lower()
            else text
        )

        self.log.info(
            f"Typing '{masked_text}' into {label or locator}"
        )

        # Wait for visible element
        element = self.wait_for_visible(locator)

        # Clear existing text
        element.clear()

        # Type new text
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        """
        Return text from element
        """

        # Get visible element text
        text = self.wait_for_visible(locator).text.strip()

        self.log.info(f"Element text: {text}")

        return text

    def get_attribute(
        self,
        locator: tuple,
        attribute_name: str
    ) -> str:
        """
        Return attribute value from element
        """

        # Get attribute value
        value = self.wait_for_present(locator).get_attribute(
            attribute_name
        )

        self.log.info(
            f"Attribute '{attribute_name}' = {value}"
        )

        return value

    def is_displayed(self, locator: tuple) -> bool:
        """
        Check whether element is visible
        """

        try:
            # Check element visibility
            result = self.wait_for_visible(locator).is_displayed()

            self.log.info(
                f"Element displayed: {result}"
            )

            return result

        except (TimeoutException, NoSuchElementException):

            self.log.warning(
                "Element is not displayed"
            )

            return False