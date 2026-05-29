"""Расширенные тесты секции Elements: Links, Upload/Download, Dynamic Properties.

Покрывает оставшиеся 3 страницы из 8 в разделе Elements.
"""

import os
import tempfile

import pytest
from playwright.sync_api import Page

from pages.elements.dynamic_properties_page import DynamicPropertiesPage
from pages.elements.links_page import LinksPage
from pages.elements.upload_download_page import UploadDownloadPage


class TestLinks:
    """Тесты для страницы Links — навигационные ссылки и API-запросы."""

    @pytest.mark.smoke
    def test_simple_link_opens_new_tab(self, page: Page) -> None:
        """TC-L01: Простая ссылка Home открывает новую вкладку с demoqa.com."""
        links = LinksPage(page).open()

        url = links.open_simple_link_in_new_tab()

        assert "demoqa.com" in url, f"Новая вкладка открылась не на demoqa.com: '{url}'"

    @pytest.mark.regression
    def test_api_link_created_returns_201(self, page: Page) -> None:
        """TC-L02: API ссылка 'Created' возвращает статус 201."""
        links = LinksPage(page).open()

        links.click_api_link("created")

        status = links.get_response_status()
        assert status == 201, f"Ожидался статус 201, получен: {status}"

    @pytest.mark.regression
    def test_api_link_no_content_returns_204(self, page: Page) -> None:
        """TC-L03: API ссылка 'No Content' возвращает статус 204."""
        links = LinksPage(page).open()

        links.click_api_link("no-content")

        status = links.get_response_status()
        assert status == 204, f"Ожидался статус 204, получен: {status}"

    @pytest.mark.regression
    def test_api_link_bad_request_returns_400(self, page: Page) -> None:
        """TC-L04: API ссылка 'Bad Request' возвращает статус 400."""
        links = LinksPage(page).open()

        links.click_api_link("bad-request")

        status = links.get_response_status()
        assert status == 400, f"Ожидался статус 400, получен: {status}"

    @pytest.mark.regression
    def test_api_link_unauthorized_returns_401(self, page: Page) -> None:
        """TC-L05: API ссылка 'Unauthorized' возвращает статус 401."""
        links = LinksPage(page).open()

        links.click_api_link("unauthorized")

        status = links.get_response_status()
        assert status == 401, f"Ожидался статус 401, получен: {status}"

    @pytest.mark.regression
    def test_api_link_forbidden_returns_403(self, page: Page) -> None:
        """TC-L06: API ссылка 'Forbidden' возвращает статус 403."""
        links = LinksPage(page).open()

        links.click_api_link("forbidden")

        status = links.get_response_status()
        assert status == 403, f"Ожидался статус 403, получен: {status}"

    @pytest.mark.regression
    def test_api_link_not_found_returns_404(self, page: Page) -> None:
        """TC-L07: API ссылка 'Not Found' возвращает статус 404."""
        links = LinksPage(page).open()

        links.click_api_link("invalid-url")

        status = links.get_response_status()
        assert status == 404, f"Ожидался статус 404, получен: {status}"


class TestUploadDownload:
    """Тесты для страницы Upload and Download."""

    @pytest.mark.smoke
    def test_download_file_success(self, page: Page) -> None:
        """TC-UD01: Скачивание файла — объект Download получен."""
        upload_download = UploadDownloadPage(page).open()

        with tempfile.TemporaryDirectory() as tmp_dir:
            dest = os.path.join(tmp_dir, "downloaded.jpg")
            saved_path = upload_download.download_and_save(dest)

            assert os.path.exists(saved_path), f"Скачанный файл не найден по пути: {saved_path}"
            assert os.path.getsize(saved_path) > 0, "Скачанный файл пустой"

    @pytest.mark.smoke
    def test_upload_file_shows_result(self, page: Page) -> None:
        """TC-UD02: Загрузка файла — результат отображается с именем файла."""
        upload_download = UploadDownloadPage(page).open()

        with tempfile.NamedTemporaryFile(suffix=".txt", prefix="test_upload_", delete=False) as tmp:
            tmp.write(b"playwright upload test")
            tmp_path = tmp.name

        try:
            upload_download.upload_file(tmp_path)

            assert upload_download.is_upload_result_visible(), "Блок результата загрузки не отображается"
            filename = upload_download.get_uploaded_filename()
            expected_name = os.path.basename(tmp_path)
            assert expected_name in filename, f"Ожидалось имя '{expected_name}' в результате, получено: '{filename}'"
        finally:
            UploadDownloadPage.remove_file(tmp_path)

    @pytest.mark.regression
    def test_download_file_has_correct_extension(self, page: Page) -> None:
        """Скачанный файл является изображением (расширение .jpeg или .png)."""
        upload_download = UploadDownloadPage(page).open()

        download = upload_download.download_file()
        filename = download.suggested_filename

        assert any(
            filename.lower().endswith(ext) for ext in (".jpeg", ".jpg", ".png")
        ), f"Неожиданное расширение скачанного файла: '{filename}'"

    @pytest.mark.regression
    def test_upload_different_file_types(self, page: Page) -> None:
        """Загрузка файла с расширением .csv — принимается формой."""
        upload_download = UploadDownloadPage(page).open()

        with tempfile.NamedTemporaryFile(suffix=".csv", prefix="test_csv_", delete=False) as tmp:
            tmp.write(b"id,name,email\n1,John,john@test.com")
            tmp_path = tmp.name

        try:
            upload_download.upload_file(tmp_path)

            assert upload_download.is_upload_result_visible(), "CSV файл не принят формой загрузки"
        finally:
            UploadDownloadPage.remove_file(tmp_path)


class TestDynamicProperties:
    """Тесты для страницы Dynamic Properties — отложенные изменения элементов.

    Ключевой сценарий: демонстрирует корректные стратегии ожидания
    вместо неустойчивых time.sleep().
    """

    @pytest.mark.smoke
    def test_enable_button_initially_disabled(self, page: Page) -> None:
        """TC-D01: Кнопка 'Will enable 5 seconds' изначально неактивна."""
        dynamic = DynamicPropertiesPage(page).open()

        assert not dynamic.is_enable_button_enabled(), "Кнопка должна быть disabled при открытии страницы"

    @pytest.mark.regression
    @pytest.mark.slow
    def test_button_becomes_enabled_after_delay(self, page: Page) -> None:
        """TC-D02: Кнопка активируется через 5 секунд (без sleep — через wait_for_function)."""
        dynamic = DynamicPropertiesPage(page).open()

        dynamic.wait_for_button_enabled()

        assert dynamic.is_enable_button_enabled(), "Кнопка не активировалась за отведённое время"

    @pytest.mark.regression
    def test_visible_button_not_present_initially(self, page: Page) -> None:
        """TC-D03: Кнопка 'Visible After 5 Seconds' изначально отсутствует в DOM."""
        dynamic = DynamicPropertiesPage(page).open()

        assert (
            not dynamic.is_visible_after_button_present()
        ), "Кнопка visibleAfter присутствует в DOM сразу, ожидалось — нет"

    @pytest.mark.regression
    @pytest.mark.slow
    def test_button_becomes_visible_after_delay(self, page: Page) -> None:
        """TC-D04: Кнопка 'Visible After 5 Seconds' появляется через 5 сек."""
        dynamic = DynamicPropertiesPage(page).open()

        dynamic.wait_for_visible_button()

        assert dynamic.is_visible_after_button_present(), "Кнопка visibleAfter не появилась за отведённое время"

    @pytest.mark.regression
    def test_color_change_button_is_present(self, page: Page) -> None:
        """Кнопка colorChange присутствует на странице с момента загрузки."""
        dynamic = DynamicPropertiesPage(page).open()

        assert dynamic.is_visible(dynamic.color_change_button), "Кнопка colorChange не видна при загрузке страницы"
