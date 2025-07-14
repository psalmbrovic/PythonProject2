import pytest
import allure
from pages.sample_page import LoginPage, HomePage
from utils.test_data_manager import TestDataManager


class TestLogin:
	"""Login functionality tests"""

	@allure.feature("Authentication")
	@allure.story("Valid Login")
	@allure.severity(allure.severity_level.CRITICAL)
	def test_valid_login(self, driver):
		"""Test valid login credentials"""
		login_page = LoginPage(driver)
		home_page = HomePage(driver)

		# Test data
		username = "testuser@example.com"
		password = "testpassword123"

		# Test steps
		with allure.step("Open login page"):
			login_page.open_login_page()

		with allure.step("Enter valid credentials"):
			login_page.login(username, password)

		with allure.step("Verify successful login"):
			assert login_page.is_login_successful(), "Login should be successful"
			assert home_page.is_user_logged_in(), "User should be logged in"

	@allure.feature("Authentication")
	@allure.story("Invalid Login")
	@allure.severity(allure.severity_level.CRITICAL)
	def test_invalid_login(self, driver):
		"""Test invalid login credentials"""
		login_page = LoginPage(driver)

		# Test data
		username = "invalid@example.com"
		password = "wrongpassword"

		# Test steps
		with allure.step("Open login page"):
			login_page.open_login_page()

		with allure.step("Enter invalid credentials"):
			login_page.login(username, password)

		with allure.step("Verify login failure"):
			error_message = login_page.get_error_message()
			assert error_message != "", "Error message should be displayed"
			assert not login_page.is_login_successful(), "Login should fail"

	@allure.feature("Authentication")
	@allure.story("Empty Credentials")
	@allure.severity(allure.severity_level.NORMAL)
	@pytest.mark.parametrize("username,password,expected_error", [
		("", "", "Username and password are required"),
		("user@test.com", "", "Password is required"),
		("", "password123", "Username is required")
	])
	def test_empty_credentials(self, driver, username, password, expected_error):
		"""Test login with empty credentials"""
		login_page = LoginPage(driver)

		with allure.step("Open login page"):
			login_page.open_login_page()

		with allure.step(f"Enter credentials: {username}, {password}"):
			login_page.login(username, password)

		with allure.step("Verify appropriate error message"):
			error_message = login_page.get_error_message()
			assert expected_error.lower() in error_message.lower()