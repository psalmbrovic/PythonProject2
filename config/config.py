import os
from dataclasses import dataclass


@dataclass
class TestConfig:
    """Test configuration class"""
    PROD_BASE_URL: str = "https://business.woven.finance/login"
    STAGING_PROD_BASE_URL: str = "https://business.staging.woven.finance/login"
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
            PROD_BASE_URL=os.getenv("PROD_BASE_URL", cls().PROD_BASE_URL),
            STAGING_PROD_BASE_URL=os.getenv("STAGING_PROD_BASE_URL", cls().STAGING_PROD_BASE_URL),
            BROWSER=os.getenv("BROWSER", cls().BROWSER).lower(),
            HEADLESS=os.getenv("HEADLESS", str(cls().HEADLESS)).lower() == "true",
            IMPLICIT_WAIT=int(os.getenv("IMPLICIT_WAIT", cls().IMPLICIT_WAIT)),
            EXPLICIT_WAIT=int(os.getenv("EXPLICIT_WAIT", cls().EXPLICIT_WAIT)),
            PAGE_LOAD_TIMEOUT=int(os.getenv("PAGE_LOAD_TIMEOUT", cls().PAGE_LOAD_TIMEOUT)),
            SCREENSHOT_ON_FAILURE=os.getenv("SCREENSHOT_ON_FAILURE", str(cls().SCREENSHOT_ON_FAILURE)).lower() == "true",
            REPORTS_DIR=os.getenv("REPORTS_DIR", cls().REPORTS_DIR),
            SCREENSHOTS_DIR=os.getenv("SCREENSHOTS_DIR", cls().SCREENSHOTS_DIR),
            TEST_DATA_DIR=os.getenv("TEST_DATA_DIR", cls().TEST_DATA_DIR),
            LOG_LEVEL=os.getenv("LOG_LEVEL", cls().LOG_LEVEL)
        )

# Instantiate config after class definition
config = TestConfig.from_env()




# import os
# from dataclasses import dataclass
# from typing import Dict, Any


# @dataclass
# class TestConfig:
# 	"""Test configuration class"""
# 	PROD_BASE_URL: str = "https://business.woven.finance/login"
# 	STAGING_PROD_BASE_URL: str = "https://business.staging.woven.finance/login"
# 	BROWSER: str = "chrome"  # chrome, firefox, edge
# 	HEADLESS: bool = False
# 	IMPLICIT_WAIT: int = 10
# 	EXPLICIT_WAIT: int = 20
# 	PAGE_LOAD_TIMEOUT: int = 30
# 	SCREENSHOT_ON_FAILURE: bool = True
# 	REPORTS_DIR: str = "reports"
# 	SCREENSHOTS_DIR: str = "screenshots"
# 	TEST_DATA_DIR: str = "test_data"
# 	LOG_LEVEL: str = "INFO"

# @classmethod
# def from_env(cls) -> 'TestConfig':
#         """Create config from environment variables"""
#         return cls(
#             PROD_BASE_URL=os.getenv("PROD_BASE_URL", cls().PROD_BASE_URL),
#             BROWSER=os.getenv("BROWSER", cls().BROWSER).lower(),
#             HEADLESS=os.getenv("HEADLESS", str(cls().HEADLESS)).lower() == "true",
#             IMPLICIT_WAIT=int(os.getenv("IMPLICIT_WAIT", cls().IMPLICIT_WAIT)),
#             EXPLICIT_WAIT=int(os.getenv("EXPLICIT_WAIT", cls().EXPLICIT_WAIT)),
#             SCREENSHOT_ON_FAILURE=os.getenv("SCREENSHOT_ON_FAILURE", str(cls().SCREENSHOT_ON_FAILURE)).lower() == "true"
#         )

# # Must come AFTER the class definition
# config = TestConfig.from_env()

# 	@classmethod
# 	def from_env(cls) -> 'TestConfig':
# 		"""Create config from environment variables"""
# 		return cls(
# 			PROD_BASE_URL=os.getenv("PROD_BASE_URL", cls.PROD_BASE_URL),
# 			BROWSER=os.getenv("BROWSER", cls.BROWSER).lower(),
# 			HEADLESS=os.getenv("HEADLESS", "false").lower() == "true",
# 			IMPLICIT_WAIT=int(os.getenv("IMPLICIT_WAIT", cls.IMPLICIT_WAIT)),
# 			EXPLICIT_WAIT=int(os.getenv("EXPLICIT_WAIT", cls.EXPLICIT_WAIT)),
# 			SCREENSHOT_ON_FAILURE=os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
# 		)


# config = TestConfig.from_env()