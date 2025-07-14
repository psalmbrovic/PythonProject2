import pytest
import allure
from pages.sample_page import HomePage


class TestSearch:
	"""Search functionality tests"""

	@allure.feature("Search")
	@allure.story("Basic Search")
	@allure.severity(allure.severity_level.NORMAL)
	def test_basic_search(self, driver):
		"""Test basic search functionality"""
		home_page = HomePage(driver)

		search_query = "selenium testing"

		with allure.step("Open home page"):
			home_page.open()

		with allure.step(f"Search for: {search_query}"):
			home_page.search(search_query)

		with allure.step("Verify search results"):
			# Add assertions based on your application
			assert "search" in home_page.get_current_url().lower()

	@allure.feature("Search")
	@allure.story("Empty Search")
	@allure.severity(allure.severity_level.MINOR)
	def test_empty_search(self, driver):
		"""Test search with empty query"""
		home_page = HomePage(driver)

		with allure.step("Open home page"):
			home_page.open()

		with allure.step("Perform empty search"):
			home_page.search("")

		with allure.step("Verify behavior"):
			# Add assertions based on expected behavior
			current_url = home_page.get_current_url()
			assert current_url is not None
