from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import logging

from config.config import config

logger = logging.getLogger(__name__)


class DriverFactory:
	"""Factory class for creating WebDriver instances"""

	@staticmethod
	def create_driver(browser: str = "chrome", headless: bool = False) -> webdriver:
		"""Create and return WebDriver instance"""
		driver = None

		try:
			if browser.lower() == "chrome":
				driver = DriverFactory._create_chrome_driver(headless)
			elif browser.lower() == "firefox":
				driver = DriverFactory._create_firefox_driver(headless)
			elif browser.lower() == "edge":
				driver = DriverFactory._create_edge_driver(headless)
			else:
				raise ValueError(f"Unsupported browser: {browser}")

			# Set timeouts
			driver.implicitly_wait(config.IMPLICIT_WAIT)
			driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)

			logger.info(f"Created {browser} driver successfully")
			return driver

		except Exception as e:
			logger.error(f"Failed to create {browser} driver: {str(e)}")
			if driver:
				driver.quit()
			raise

	@staticmethod
	def _create_chrome_driver(headless: bool) -> webdriver.Chrome:
		"""Create Chrome WebDriver"""
		options = ChromeOptions()
		if headless:
			options.add_argument("--headless")
		options.add_argument("--no-sandbox")
		options.add_argument("--disable-dev-shm-usage")
		options.add_argument("--disable-gpu")
		options.add_argument("--window-size=1920,1080")

		service = ChromeService(ChromeDriverManager().install())
		return webdriver.Chrome(service=service, options=options)

	@staticmethod
	def _create_firefox_driver(headless: bool) -> webdriver.Firefox:
		"""Create Firefox WebDriver"""
		options = FirefoxOptions()
		if headless:
			options.add_argument("--headless")
		options.add_argument("--width=1920")
		options.add_argument("--height=1080")

		service = FirefoxService(GeckoDriverManager().install())
		return webdriver.Firefox(service=service, options=options)

	@staticmethod
	def _create_edge_driver(headless: bool) -> webdriver.Edge:
		"""Create Edge WebDriver"""
		options = EdgeOptions()
		if headless:
			options.add_argument("--headless")
		options.add_argument("--no-sandbox")
		options.add_argument("--disable-dev-shm-usage")
		options.add_argument("--window-size=1920,1080")

		service = EdgeService(EdgeChromiumDriverManager().install())
		return webdriver.Edge(service=service, options=options)