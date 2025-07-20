from selenium.webdriver.common.by import By
from base.base_page import BasePage


class LoginPage(BasePage):
	""" login page object"""

	# Locators Prod
	USERNAME_INPUT = (By.XPATH, "//Input[@placeholder='Email Address']")
	PASSWORD_INPUT = (By.XPATH, "//Input[@placeholder='Password']")
	LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
	ERROR_MESSAGE = (By.XPATH, "error-message")
	FORGOT_PASSWORD_LINK = (By.XPATH, "//a[@href='/password-reset']")
	

	# # Locators Staging
	# USERNAME_INPUT = (By.ID, "username")
	# PASSWORD_INPUT = (By.ID, "password")
	# LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
	# ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
	# FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")

	def __init__(self, driver):
		super().__init__(driver)
		self.page_url = f"{self.driver.current_url}/login"

	def open_login_page(self):
		"""Open login page"""
		self.open(self.page_url)
		self.wait_for_page_load()

	def enter_username(self, username: str):
		"""Enter username"""
		self.send_keys(self.USERNAME_INPUT, username)

	def enter_password(self, password: str):
		"""Enter password"""
		self.send_keys(self.PASSWORD_INPUT, password)

	def click_login_button(self):
		"""Click login button"""
		self.click(self.LOGIN_BUTTON)

	def login(self, username: str, password: str):
		"""Complete login process"""
		self.enter_username(username)
		self.enter_password(password)
		self.click_login_button()

	def get_error_message(self) -> str:
		"""Get error message text"""
		if self.is_element_visible(self.ERROR_MESSAGE):
			return self.get_text(self.ERROR_MESSAGE)
		return ""

	def is_login_successful(self) -> bool:
		"""Check if login was successful"""
		# Assuming successful login redirects to dashboard
		return "dashboard" in self.get_current_url().lower()


class HomePage(BasePage):
	"""Sample home page object"""

	# Locators
	SEARCH_BOX = (By.NAME, "search")
	SEARCH_BUTTON = (By.XPATH, "//button[contains(text(), 'Search')]")
	USER_MENU = (By.ID, "user-menu")
	LOGOUT_LINK = (By.LINK_TEXT, "Logout")
	NAVIGATION_MENU = (By.CLASS_NAME, "nav-menu")

	def search(self, query: str):
		"""Perform search"""
		self.send_keys(self.SEARCH_BOX, query)
		self.click(self.SEARCH_BUTTON)

	def logout(self):
		"""Logout user"""
		self.click(self.USER_MENU)
		self.click(self.LOGOUT_LINK)

	def is_user_logged_in(self) -> bool:
		"""Check if user is logged in"""
		return self.is_element_present(self.USER_MENU)