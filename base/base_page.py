from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
from datetime import datetime
from config.config import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class BasePage:
	"""Base page class with common page operations"""

	def __init__(self, driver):
		self.driver = driver
		self.wait = WebDriverWait(driver, config.EXPLICIT_WAIT)
		self.actions = ActionChains(driver)

	def open(self, url: str = None):
		"""Open URL in browser"""
		url = url or config.BASE_URL
		logger.info(f"Opening URL: {url}")
		self.driver.get(url)

	def find_element(self, locator: tuple, timeout: int = None):
		"""Find element with explicit wait"""
		timeout = timeout or config.EXPLICIT_WAIT
		try:
			wait = WebDriverWait(self.driver, timeout)
			element = wait.until(EC.presence_of_element_located(locator))
			logger.debug(f"Found element: {locator}")
			return element
		except TimeoutException:
			logger.error(f"Element not found: {locator}")
			self.take_screenshot("element_not_found")
			raise

	def find_elements(self, locator: tuple, timeout: int = None):
		"""Find multiple elements"""
		timeout = timeout or config.EXPLICIT_WAIT
		try:
			wait = WebDriverWait(self.driver, timeout)
			elements = wait.until(EC.presence_of_all_elements_located(locator))
			logger.debug(f"Found {len(elements)} elements: {locator}")
			return elements
		except TimeoutException:
			logger.error(f"Elements not found: {locator}")
			return []

	def click(self, locator: tuple, timeout: int = None):
		"""Click element"""
		element = self.wait_for_clickable(locator, timeout)
		try:
			element.click()
			logger.info(f"Clicked element: {locator}")
		except Exception as e:
			logger.error(f"Failed to click element {locator}: {str(e)}")
			self.take_screenshot("click_failed")
			raise

	def send_keys(self, locator: tuple, text: str, clear: bool = True, timeout: int = None):
		"""Send keys to element"""
		element = self.find_element(locator, timeout)
		try:
			if clear:
				element.clear()
			element.send_keys(text)
			logger.info(f"Sent keys '{text}' to element: {locator}")
		except Exception as e:
			logger.error(f"Failed to send keys to element {locator}: {str(e)}")
			self.take_screenshot("send_keys_failed")
			raise

	def get_text(self, locator: tuple, timeout: int = None) -> str:
		"""Get text from element"""
		element = self.find_element(locator, timeout)
		text = element.text
		logger.debug(f"Got text '{text}' from element: {locator}")
		return text

	def get_attribute(self, locator: tuple, attribute: str, timeout: int = None) -> str:
		"""Get attribute value from element"""
		element = self.find_element(locator, timeout)
		value = element.get_attribute(attribute)
		logger.debug(f"Got attribute '{attribute}' value '{value}' from element: {locator}")
		return value

	def is_element_present(self, locator: tuple, timeout: int = 5) -> bool:
		"""Check if element is present"""
		try:
			wait = WebDriverWait(self.driver, timeout)
			wait.until(EC.presence_of_element_located(locator))
			return True
		except TimeoutException:
			return False

	def is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
		"""Check if element is visible"""
		try:
			wait = WebDriverWait(self.driver, timeout)
			wait.until(EC.visibility_of_element_located(locator))
			return True
		except TimeoutException:
			return False

	def wait_for_clickable(self, locator: tuple, timeout: int = None):
		"""Wait for element to be clickable"""
		timeout = timeout or config.EXPLICIT_WAIT
		try:
			wait = WebDriverWait(self.driver, timeout)
			return wait.until(EC.element_to_be_clickable(locator))
		except TimeoutException:
			logger.error(f"Element not clickable: {locator}")
			self.take_screenshot("element_not_clickable")
			raise

	def select_dropdown_by_text(self, locator: tuple, text: str, timeout: int = None):
		"""Select dropdown option by visible text"""
		element = self.find_element(locator, timeout)
		select = Select(element)
		select.select_by_visible_text(text)
		logger.info(f"Selected dropdown option '{text}' for element: {locator}")

	def select_dropdown_by_value(self, locator: tuple, value: str, timeout: int = None):
		"""Select dropdown option by value"""
		element = self.find_element(locator, timeout)
		select = Select(element)
		select.select_by_value(value)
		logger.info(f"Selected dropdown value '{value}' for element: {locator}")

	def hover(self, locator: tuple, timeout: int = None):
		"""Hover over element"""
		element = self.find_element(locator, timeout)
		self.actions.move_to_element(element).perform()
		logger.info(f"Hovered over element: {locator}")

	def scroll_to_element(self, locator: tuple, timeout: int = None):
		"""Scroll to element"""
		element = self.find_element(locator, timeout)
		self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
		time.sleep(1)  # Wait for scroll to complete
		logger.info(f"Scrolled to element: {locator}")

	def wait_for_page_load(self, timeout: int = None):
		"""Wait for page to load completely"""
		timeout = timeout or config.PAGE_LOAD_TIMEOUT
		wait = WebDriverWait(self.driver, timeout)
		wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
		logger.info("Page loaded completely")

	def take_screenshot(self, name: str = None) -> str:
		"""Take screenshot and return file path"""
		if not config.SCREENSHOT_ON_FAILURE and name != "manual":
			return ""

		os.makedirs(config.SCREENSHOTS_DIR, exist_ok=True)
		timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
		name = name or "screenshot"
		filename = f"{name}_{timestamp}.png"
		filepath = os.path.join(config.SCREENSHOTS_DIR, filename)

		try:
			self.driver.save_screenshot(filepath)
			logger.info(f"Screenshot saved: {filepath}")
			return filepath
		except Exception as e:
			logger.error(f"Failed to take screenshot: {str(e)}")
			return ""

	def get_current_url(self) -> str:
		"""Get current URL"""
		return self.driver.current_url

	def get_title(self) -> str:
		"""Get page title"""
		return self.driver.title

	def refresh_page(self):
		"""Refresh the current page"""
		self.driver.refresh()
		logger.info("Page refreshed")

	def go_back(self):
		"""Navigate back"""
		self.driver.back()
		logger.info("Navigated back")

	def go_forward(self):
		"""Navigate forward"""
		self.driver.forward()
		logger.info("Navigated forward")
