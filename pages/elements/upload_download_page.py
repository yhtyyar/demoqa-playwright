"""Страница Upload and Download — загрузка и скачивание файлов."""

import os
from pathlib import Path

from playwright.sync_api import Download, Locator, Page

from pages.base_page import BasePage


class UploadDownloadPage(BasePage):
    """Page Object для страницы https://demoqa.com/upload-download.

    Демонстрирует два Playwright-паттерна:
    - page.expect_download() для перехвата скачивания файлов.
    - set_input_files() для имитации file upload без реального диалога.
    """

    BUTTON_DOWNLOAD = "#downloadButton"
    INPUT_UPLOAD = "#uploadFile"
    UPLOAD_RESULT = "#uploadedFilePath"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "UploadDownloadPage":
        """Открыть страницу Upload and Download."""
        super().open("/upload-download")
        return self

    @property
    def upload_input(self) -> Locator:
        """Скрытый input[type=file] для загрузки."""
        return self.page.locator(self.INPUT_UPLOAD)

    @property
    def upload_result(self) -> Locator:
        """Блок с именем загруженного файла."""
        return self.page.locator(self.UPLOAD_RESULT)

    def download_file(self) -> Download:
        """Нажать Download и перехватить объект скачивания.

        Returns:
            Объект Playwright Download для дальнейшей работы (save_as, path, etc.).
        """
        with self.page.expect_download() as download_info:
            self.click(self.page.locator(self.BUTTON_DOWNLOAD))
        return download_info.value

    def download_and_save(self, dest_path: str) -> str:
        """Скачать файл и сохранить в указанный путь.

        Args:
            dest_path: Путь для сохранения файла.

        Returns:
            Путь к сохранённому файлу.
        """
        download = self.download_file()
        download.save_as(dest_path)
        return dest_path

    def upload_file(self, file_path: str) -> "UploadDownloadPage":
        """Загрузить файл через set_input_files (без диалога ОС).

        Args:
            file_path: Абсолютный путь к загружаемому файлу.

        Returns:
            Экземпляр UploadDownloadPage для chaining.
        """
        self.upload_input.set_input_files(file_path)
        self.wait_for_element(self.upload_result)
        return self

    def get_uploaded_filename(self) -> str:
        """Получить имя загруженного файла из блока результата.

        Returns:
            Имя файла (последняя часть пути).
        """
        result_text = self.get_text(self.upload_result)
        return Path(result_text).name if result_text else ""

    def is_upload_result_visible(self) -> bool:
        """Проверить, отображается ли результат загрузки."""
        return self.is_visible(self.upload_result)

    @staticmethod
    def create_temp_file(path: str, content: str = "test content") -> str:
        """Создать временный текстовый файл для теста загрузки.

        Args:
            path: Путь для создания файла.
            content: Содержимое файла.

        Returns:
            Путь к созданному файлу.
        """
        with open(path, "w") as f:
            f.write(content)
        return path

    @staticmethod
    def remove_file(path: str) -> None:
        """Удалить файл если существует."""
        if os.path.exists(path):
            os.remove(path)
