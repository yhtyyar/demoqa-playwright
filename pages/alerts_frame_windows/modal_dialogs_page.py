"""Страница Modal Dialogs — модальные окна."""

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class ModalDialogsPage(BasePage):
    """Page Object для страницы https://demoqa.com/modal-dialogs."""

    BUTTON_SMALL_MODAL = "#showSmallModal"
    BUTTON_LARGE_MODAL = "#showLargeModal"
    MODAL_TITLE = ".modal-title"
    MODAL_BODY = ".modal-body"
    CLOSE_SMALL_MODAL = "#closeSmallModal"
    CLOSE_LARGE_MODAL = "#closeLargeModal"
    MODAL_DIALOG = ".modal-dialog"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "ModalDialogsPage":
        """Открыть страницу Modal Dialogs."""
        super().open("/modal-dialogs")
        return self

    @property
    def modal_dialog(self) -> Locator:
        """Контейнер открытого модального окна."""
        return self.page.locator(self.MODAL_DIALOG)

    @property
    def modal_title(self) -> Locator:
        """Заголовок модального окна."""
        return self.page.locator(self.MODAL_TITLE)

    @property
    def modal_body(self) -> Locator:
        """Тело модального окна."""
        return self.page.locator(self.MODAL_BODY)

    def open_small_modal(self) -> "ModalDialogsPage":
        """Открыть маленькое модальное окно."""
        self.click(self.page.locator(self.BUTTON_SMALL_MODAL))
        self.wait_for_element(self.modal_dialog)
        return self

    def open_large_modal(self) -> "ModalDialogsPage":
        """Открыть большое модальное окно."""
        self.click(self.page.locator(self.BUTTON_LARGE_MODAL))
        self.wait_for_element(self.modal_dialog)
        return self

    def close_small_modal(self) -> "ModalDialogsPage":
        """Закрыть маленькое модальное окно кнопкой Close."""
        self.click(self.page.locator(self.CLOSE_SMALL_MODAL))
        self.wait_for_element(self.modal_dialog, state="hidden")
        return self

    def close_large_modal(self) -> "ModalDialogsPage":
        """Закрыть большое модальное окно кнопкой Close."""
        self.click(self.page.locator(self.CLOSE_LARGE_MODAL))
        self.wait_for_element(self.modal_dialog, state="hidden")
        return self

    def is_modal_open(self) -> bool:
        """Проверить, открыто ли модальное окно."""
        return self.is_visible(self.modal_dialog)

    def get_modal_title(self) -> str:
        """Получить заголовок открытого модального окна."""
        return self.get_text(self.modal_title)

    def get_modal_body_text(self) -> str:
        """Получить текст тела открытого модального окна."""
        return self.get_text(self.modal_body)
