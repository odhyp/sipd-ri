# TODO: add module docstring


import logging
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError


logger = logging.getLogger(__name__)


class AklapPostingJurnalMixin:
    def posting_pendapatan(self):
        """
        TODO: add docstring

        Form group list:
        - nth(0): SKPD
        - nth(1): Transaksi
        - nth(2): Status
        - nth(3): Tanggal Awal
        - nth(4): Tanggal Akhir
        - nth(5): Filter By Keyword
        """
        self.to_aklap()

        # Dashboard AKLAP - Menu Posting Jurnal
        menu_posting_jurnal = 'a.dropdown-toggle:has-text("Posting Jurnal")'
        self.ensure_element_visible(menu_posting_jurnal)
        btn_posting_jurnal = self.page.locator(menu_posting_jurnal)
        btn_posting_jurnal.click()
        logger.info("Menu Posting Jurnal opened")

        # Menu Posting Jurnal - Sub Menu Pendapatan
        submenu_pendapatan = 'a.sidebar-link:has-text("Pendapatan")'
        self.ensure_element_visible(submenu_pendapatan)
        btn_pendapatan = self.page.get_by_role("link", name="Pendapatan", exact=True)
        btn_pendapatan.click()
        logger.info("Sub Menu Pendapatan opened")

        # Sub Menu Pendapatan
        menu_body = self.page.locator("div.card-body")

        # Form Group - SKPD
        form_group_skpd = menu_body.locator("div.form-group").nth(0)
        input_skpd = form_group_skpd.locator("input")

        dev_skpd = (
            "DINAS LINGKUNGAN HIDUP DAN KEHUTANAN"  # TODO: replace with parameter
        )

        input_skpd.type(dev_skpd)
        dropdown_skpd = menu_body.locator(f'ul[role=listbox] li:has-text("{dev_skpd}")')

        try:
            dropdown_skpd.wait_for(timeout=3_000, state="visible")
            dropdown_skpd.click()
        except PlaywrightTimeoutError:
            logger.warning("Dropdown not found for SKPD: %s", dev_skpd)
            # TODO: add retry logic

        # Form Group - Transaksi
        form_group_transaksi = menu_body.locator("div.form-group").nth(1)
        input_transaksi = form_group_transaksi.locator("input")
        input_transaksi.type(
            "Penerimaan"
        )  # TODO: replace with parameter, `Penerimaan` and `Setoran`
        input_transaksi.press("Enter")

        # Form Group - Status
        form_group_status = menu_body.locator("div.form-group").nth(2)
        input_status = form_group_status.locator("input")
        input_status.type("Belum di posting/reject")
        input_status.press("Enter")

        # Form Group - Tanggal Awal (Unused)
        form_group_tanggal_awal = menu_body.locator("div.form-group").nth(3)

        # Form Group - Tanggal Akhir (Unused)
        form_group_tanggal_akhir = menu_body.locator("div.form-group").nth(4)

        # Form Group - Filter by Keyword (Unused)
        form_group_filter = menu_body.locator("div.form-group").nth(5)

        # Apply button
        btn_terapkan = menu_body.locator('button:has-text("Terapkan")')
        btn_terapkan.click()

        # Transaction table
        table = menu_body.locator("table")
        check_all = table.locator("thead th div.custom-checkbox")
        check_all.click()

        # Posting button
        btn_posting = menu_body.locator('button:has-text("Posting")')
        expect(btn_posting).to_be_enabled()
        btn_posting.click()

        # Confirmation modal
        confirmation_modal = self.page.locator("div.swal2-actions")
        confirmation_modal.wait_for()

        btn_yes = confirmation_modal.locator('button:has-text("Ya")')
        btn_yes.wait_for()
        btn_yes.click()

        btn_ok = confirmation_modal.locator('button:has-text("OK")')
        btn_ok.wait_for()
        btn_ok.click()

        # TODO: add checker when everything is posted

        input(">>>>>>>>>>>>>>>>>>>> ENTER")
