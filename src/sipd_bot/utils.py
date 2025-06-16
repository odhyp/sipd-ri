"""
This module provides the UtilityMixin class for the SIPDBot automation framework.

Includes page recovery methods such as auto-reloading, 404 detection,
and navigating to specific modules like AKLAP.
"""

import logging

logger = logging.getLogger(__name__)


class UtilsMixin:
    """
    Provides utility methods for SIPDBot
    """

    def ensure_element_visible(
        self, selector: str, retries: int = 3, delay: int = 2
    ) -> bool:
        """
        Ensure a specific selector exists on the page, reload if not found.

        Args:
            selector (str): CSS or text selector expected to exist.
            retries (int): Number of retries before giving up.
            delay (int): Seconds to wait between retries.

        Returns:
            bool: True if the selector was eventually found, False otherwise.
        """
        for attempt in range(retries):
            try:
                self.page.wait_for_selector(selector, timeout=3000)
                return True
            except Exception:
                logger.warning(
                    "Selector not found: %s (attempt %s/%s), reloading...",
                    selector,
                    attempt + 1,
                    retries,
                )
                self.page.reload()
                self.page.wait_for_timeout(delay * 1000)
        logger.error("Failed to find selector after %s retries: %s", retries, selector)
        return False

    def is_404(self) -> bool:
        """
        Check if the current page is a 404 error page.

        It looks for key elements typically on a 404 page (h1, span, and link).
        Uses `locator.wait_for(state="attached")` to ensure presence.

        Returns:
            bool: True if all these indicators are present, False otherwise.
        """
        selectors = [
            'h1:has-text("404")',
            'span:has-text("This page could not be found")',
            'a:has-text("Redirect to home page")',
        ]

        try:
            for sel in selectors:
                locator = self.page.locator(sel)
                try:
                    locator.wait_for(state="attached", timeout=2_000)
                except Exception:
                    logger.debug("404 indicator not found: %s", sel)
                    return False
            logger.warning("Page appears to be a 404 error page")
            return True

        except Exception as exc:
            logger.exception("Error while checking for 404 page: %s", exc)
            raise

    def to_aklap(self, attempts: int = 3):
        """
        Navigate to the AKLAP menu within the SIPD-RI web application.

        This method clicks the "Akuntansi" menu link and attempts to load the AKLAP
        page. If the page appears to be a 404 error, it retries up to a given number
        of attempts by reloading the URL.

        Args:
            attempts (int, optional): Maximum number of retry attempts if a 404 page
            is detected. Defaults to 3.

        Raises:
            RuntimeError: If the AKLAP page fails to load successfully after all attempts.
        """
        menu_akuntansi = 'a:has-text("Akuntansi")'

        if self.ensure_element_visible(menu_akuntansi):
            logger.info("Accessing AKLAP menu...")
            url_aklap = "https://sipd.kemendagri.go.id/penatausahaan/aklap"
            self.page.goto(url_aklap)

            for attempt in range(attempts):
                if not self.is_404():
                    break
                logger.warning(
                    "Reloading AKLAP page (attempt %s/%s)", attempt + 1, attempts
                )
                self.page.goto(url_aklap)
            else:
                logger.error("Failed to load AKLAP after %s attempts", attempts)
                raise RuntimeError("Could not load AKLAP page")

            logger.info("AKLAP menu accessed")
