import os
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class TestConfig:
	"""Test configuration class"""
	BASE_URL: str = "https://example.com"
	BROWSER: str = "chrome"  # chrome, firefox, edge
	HEADLESS: bool = False
	IMPLICIT_WAIT: int = 10
	EXPLICIT_WAIT: int = 20
	PAGE_LOAD_TIMEOUT: int = 30
	SCREENSHOT_ON_FAILURE: bool = True
	REPORTS_DIR: str = "reports"
	SCREENSHOTS_DIR: str = "screenshots"
	TEST_DATA_DIR: str = "test_data"
	LOG_LEVEL: str = "INFO"

	@classmethod
	def from_env(cls) -> 'TestConfig':
		"""Create config from environment variables"""
		return cls(
			BASE_URL=os.getenv("BASE_URL", cls.BASE_URL),
			BROWSER=os.getenv("BROWSER", cls.BROWSER).lower(),
			HEADLESS=os.getenv("HEADLESS", "false").lower() == "true",
			IMPLICIT_WAIT=int(os.getenv("IMPLICIT_WAIT", cls.IMPLICIT_WAIT)),
			EXPLICIT_WAIT=int(os.getenv("EXPLICIT_WAIT", cls.EXPLICIT_WAIT)),
			SCREENSHOT_ON_FAILURE=os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
		)


config = TestConfig.from_env()