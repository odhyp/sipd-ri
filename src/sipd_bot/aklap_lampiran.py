import logging


logger = logging.getLogger(__name__)


class AklapLampiranMixin:
    def download_lampiran_perkada(self, output_dir: str, skpd_list: list):
        self.to_aklap()
        # TODO: add file select for skpd list
        # TODO: implement self.ensure_element_visible in aklap_jurnal_umum.py

        # Dashboard AKLAP
        btn_lampiran = self.page.get_by_role("link", name="LPPD", exact=True)
        btn_lampiran.click()
        logger.info("Menu Perkada opened")

        # Lampiran I.1 (Perkada) Menu
        lampiran_perkada_row = self.page.locator(
            'tr:has-text("Lampiran I.1 (Perkada)")'
        )
        lampiran_perkada_row.wait_for()
        btn_cetak = lampiran_perkada_row.locator('button:has-text("Cetak")')
        btn_cetak.click()

        # Modal Pop-up
        modal_body = self.page.locator("div.modal-body")
        modal_body.wait_for()

        # Modal Fieldsets
        fieldset_skpd = modal_body.locator("fieldset").nth(0)
        fieldset_konsolidasi = modal_body.locator("fieldset").nth(1)
        fieldset_radio = modal_body.locator("fieldset").nth(2)

        for skpd in skpd_list:
            # 1. SKPD
            dropdown_skpd = fieldset_skpd.locator("input").first
            dropdown_skpd.click()
            dropdown_skpd.type(skpd)
            dropdown_skpd.press("Enter")

            # 2. Konsolidasi SKPD
            dropdown_konsolidasi = fieldset_konsolidasi.locator("input").first
            dropdown_konsolidasi.click()
            dropdown_konsolidasi.type("SKPD dan Unit")
            dropdown_konsolidasi.press("Enter")

            # 3. Radio button
            # TODO: add radio button logic
            # radio_konsolidasi = fieldset_radio.locator("label").nth(0)
            # radio_konsolidasi.click()

            radio_per_skpd = fieldset_radio.locator("label").nth(1)
            radio_per_skpd.click()

            # 4. Cetak Button
            modal_footer = self.page.locator("footer.modal-footer")
            btn_cetak = modal_footer.locator("button.dropdown-toggle")
            btn_cetak.click()

            # 4.1 Cetak Button - Download PDF
            with self.page.expect_download(
                timeout=60_000
            ) as download_info:  # TODO: set download timeout as method parameter
                option_pdf = modal_footer.locator('a.dropdown-item:has-text("PDF")')
                option_pdf.wait_for()
                option_pdf.click()

            download_name = f"Lampiran I.1 - {skpd}.pdf"
            download_path = f"{output_dir}/{download_name}"

            download_file = download_info.value
            download_file.save_as(download_path)

            logger.info("Successful download: %s", skpd)

        logger.debug("Download Lampiran Perkada has successfully ran")
