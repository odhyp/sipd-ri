"""
This module provides the AklapJurnalUmumMixin class for the SIPDBot automation framework.

It encapsulates all functionality related to 'Jurnal Umum' menu in AKLAP.
"""

import logging
import pandas as pd
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


logger = logging.getLogger(__name__)


class AklapJurnalUmumMixin:
    """
    Provides automation functionality for the 'Jurnal Umum' section of AKLAP.
    """

    def input_jurnal_umum(self, jurnal_umum: list):
        """
        Automates the process of inputting multiple 'Jurnal Umum' records into the AKLAP system.

        Parameters:
            jurnal_umum (list): A list of journal entries, where each entry is a list containing
                                [kode_rekening, debit, kredit].

        Behavior:
            - Navigates to the Jurnal Umum menu and selects the 'Input Jurnal Umum' tab.
            - For each entry:
                - Inputs 'Kode Rekening' with dropdown selection (with retry mechanism).
                - Fills in Debit and/or Kredit values if present.
                - Clicks the 'Tambah' button to add the entry.
            - Prompts the user at the start and end of the process for manual confirmation.
        """
        self.to_aklap()
        menu_jurnal_umum = 'a.sidebar-link:has-text("Jurnal Umum")'
        self.ensure_element_visible(menu_jurnal_umum)

        # Dashboard AKLAP
        btn_jurnal_umum = self.page.get_by_role("link", name="Jurnal Umum", exact=True)
        btn_jurnal_umum.click()
        logger.info("Menu Jurnal Umum opened")

        # Menu Jurnal Umum - Tab Input Jurnal Umum
        tab_header = self.page.locator("div.card-header")
        tablist_input = tab_header.locator('a:has-text("Input Jurnal Umum")')
        tablist_input.click()

        # Manual User Input
        print("\nIsi form Jurnal Umum!")
        input("Tekan Enter untuk mengisi Jurnal secara otomatis...")

        # Input Start
        tab_content = self.page.locator("div.tab-content")
        tabpanel_input = tab_content.locator("div.active")

        for jurnal in jurnal_umum:
            kode_rekening = jurnal[0]
            debit = jurnal[1]
            kredit = jurnal[2]

            # Kode Rekening
            max_retries = 5
            input_kode_rekening = tabpanel_input.locator(
                'fieldset:has-text("Kode Rekening") input'
            )
            input_kode_rekening.scroll_into_view_if_needed()

            for attempt in range(max_retries):
                input_kode_rekening.click()
                input_kode_rekening.type(kode_rekening)
                dropdown_kode_rekening = tabpanel_input.locator(
                    f'fieldset:has-text("Kode Rekening") ul[role="listbox"] li:has-text("{kode_rekening}")'
                )

                try:
                    dropdown_kode_rekening.wait_for(timeout=10_000, state="visible")
                    dropdown_kode_rekening.click()
                    break
                except PlaywrightTimeoutError:
                    logger.warning(
                        "Dropdown not found for kode: %s, retrying attempt [%d/%d]",
                        kode_rekening,
                        attempt + 1,
                        max_retries,
                    )
                    input_kode_rekening.fill("")
                    check_dropdown = tabpanel_input.locator(
                        'fieldset:has-text("Kode Rekening") ul[role="listbox"]'
                    )
                    check_dropdown.wait_for(timeout=3_000, state="visible")
            else:
                logger.error(
                    "Skipping kode rekening: %s (After %d attempts)",
                    kode_rekening,
                    max_retries,
                )
                continue

            # Debit
            if not pd.isna(debit):
                input_debit = tabpanel_input.locator('fieldset:has-text("Debit") input')
                input_debit.click()
                input_debit.type(debit)

            # Kredit
            if not pd.isna(kredit):
                input_kredit = tabpanel_input.locator(
                    'fieldset:has-text("Kredit") input'
                )
                input_kredit.click()
                input_kredit.type(kredit)

            # Tambah
            btn_tambah = tabpanel_input.locator('fieldset button:has-text("Tambah")')
            btn_tambah.scroll_into_view_if_needed()
            btn_tambah.click()

        # Input Finished
        print("\nJangan lupa untuk tekan tombol Simpan!")
        input("Tekan Enter untuk kembali...")
