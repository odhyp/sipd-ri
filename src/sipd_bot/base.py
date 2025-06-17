"""
This module provides the SIPDBotBase class, which serves as a foundational context manager
for browser automation tasks using Playwright. It handles the setup and teardown of the
browser, context, and page objects, allowing derived classes to focus on automation logic
without managing browser lifecycle details.
"""

import logging
import traceback as tb
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)


class SIPDBotBase:
    """
    Base class for SIPDBot providing browser automation context management.

    This class encapsulates the initialization and cleanup of Playwright's browser,
    context, and page objects. It is intended to be used as a context manager,
    ensuring that resources are properly allocated and released.

    Attributes:
        browser: The Playwright browser instance.
        context: The browser context for managing settings and cookies.
        page: The active page for navigation and interaction.
        playwright: The Playwright instance.
    """

    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None
        logger.debug("SIPDBotBase initialized")

    def __enter__(self):
        """
        Initializes the browser and page when entering the context.

        Attributes:
            self.browser (Browser): The Playwright browser instance.
            self.context (BrowserContext): The context for managing browser settings and cookies.
            self.page (Page): The active page within the browser context for navigation and
                            interaction.

        Notes:
            - The browser is launched in non-headless mode (`headless=False`) to allow visual
            debugging.
            - The `--start-maximized` argument ensures the browser opens in maximized mode.
            - The default viewport is disabled using `no_viewport=True` to allow full screen.
        """
        logger.debug("Starting Playwright...")
        self.playwright = sync_playwright().start()

        headless = False
        browser_args = ["--start-maximized"]
        self.browser = self.playwright.chromium.launch(
            headless=headless, args=browser_args
        )
        self.context = self.browser.new_context(no_viewport=True)
        self.page = self.context.new_page()
        logger.info(
            "Browser launched with headless=%s and args=%s", headless, browser_args
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Closes the browser and cleans up resources when exiting the context.
        """
        if self.context:
            logger.debug("Closing context...")
            self.context.close()
        if self.browser:
            logger.debug("Closing browser...")
            self.browser.close()
        if self.playwright:
            logger.debug("Stopping Playwright...")
            self.playwright.stop()
            logger.info("Browser closed")
        if exc_type:
            logger.warning("Exception occurred during session: %s", exc_value)
            logger.debug("Traceback:\n%s", "".join(tb.format_tb(traceback)))
        logger.debug("SIPDBotBase session ended")
