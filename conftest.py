import pytest
import os
from datetime import datetime
from selenium import webdriver
from utils.driver_factory import DriverFactory
from config.config import config
from utils.logger import setup_logger
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from reports.html_report_generator import HTMLReportGenerator
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

logger = setup_logger(__name__)

# Test results collector
test_results = []


@pytest.fixture(scope="function")
def driver():
    """WebDriver fixture"""
    driver = None
    try:
        if config.BROWSER.lower() == "chrome":
            chrome_options = webdriver.ChromeOptions()
            if config.HEADLESS:
                chrome_options.add_argument("--headless=new")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--window-size=1920,1080")
            # service = ChromeService(ChromeDriverManager().install())
            service = ChromeService("/Users/abatansamuel/Desktop/My_AUTO_WORK/PythonProject2/drivers/chromedriver")
            driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("WebDriver (Chrome) created successfully")
        else:
            raise ValueError(f"Unsupported browser: {config.BROWSER}")

        yield driver

    except Exception as e:
        logger.error(f"Failed to create WebDriver: {str(e)}")
        raise

    finally:
        if driver:
            driver.quit()
            logger.info("WebDriver closed successfully")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
	"""Hook to capture test results"""
	outcome = yield
	report = outcome.get_result()

	if report.when == "call":
		test_result = {
			'test_name': item.name,
			'test_class': item.cls.__name__ if item.cls else 'N/A',
			'status': 'PASSED' if report.passed else 'FAILED' if report.failed else 'SKIPPED',
			'duration': getattr(report, 'duration', 0),
			'error_message': str(report.longrepr) if report.failed else '',
			'screenshot': ''
		}

		# Take screenshot on failure
		if report.failed and hasattr(item, 'funcargs') and 'driver' in item.funcargs:
			try:
				driver = item.funcargs['driver']
				screenshot_path = driver.save_screenshot(
					f"screenshots/failed_{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
				)
				test_result['screenshot'] = screenshot_path
			except Exception as e:
				logger.error(f"Failed to take screenshot: {str(e)}")

		test_results.append(test_result)


def pytest_sessionfinish(session, exitstatus):
	"""Generate custom HTML report after test session"""
	try:
		report_generator = HTMLReportGenerator()
		report_path = report_generator.generate_report(test_results)
		logger.info(f"Custom HTML report generated: {report_path}")
		print(f"\n📊 Custom HTML Report: {os.path.abspath(report_path)}")
	except Exception as e:
		logger.error(f"Failed to generate custom HTML report: {str(e)}")
