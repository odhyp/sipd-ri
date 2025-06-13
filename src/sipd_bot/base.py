"""
This module provides the SIPDBotBase class, which serves as a foundational context manager
for browser automation tasks using Playwright. It handles the setup and teardown of the
browser, context, and page objects, allowing derived classes to focus on automation logic
without managing browser lifecycle details.
"""

from playwright.sync_api import sync_playwright


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
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=False, args=["--start-maximized"]
        )
        self.context = self.browser.new_context(no_viewport=True)
        self.page = self.context.new_page()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Closes the browser and cleans up resources when exiting the context.
        """
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
