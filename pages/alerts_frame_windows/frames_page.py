"""Страницы Frames и Nested Frames — работа с iframe."""

from playwright.sync_api import Frame, Locator, Page

from pages.base_page import BasePage


class FramesPage(BasePage):
    """Page Object для страницы https://demoqa.com/frames.

    Два независимых фрейма. Демонстрирует доступ к содержимому iframe
    через page.frame_locator() — типичная задача при тестировании legacy UI.
    """

    FRAME1 = "#frame1"
    FRAME2 = "#frame2"
    HEADING_IN_FRAME = "#sampleHeading"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "FramesPage":
        """Открыть страницу Frames."""
        super().open("/frames")
        return self

    def get_frame1_text(self) -> str:
        """Получить текст заголовка из первого фрейма.

        Returns:
            Текст #sampleHeading внутри frame1.
        """
        return (
            self.page.frame_locator(self.FRAME1)
            .locator(self.HEADING_IN_FRAME)
            .text_content() or ""
        )

    def get_frame2_text(self) -> str:
        """Получить текст заголовка из второго фрейма.

        Returns:
            Текст #sampleHeading внутри frame2.
        """
        return (
            self.page.frame_locator(self.FRAME2)
            .locator(self.HEADING_IN_FRAME)
            .text_content() or ""
        )

    def get_frame_by_id(self, frame_id: str) -> Frame:
        """Получить объект Frame по id атрибуту.

        Args:
            frame_id: Значение id-атрибута фрейма (без #).

        Returns:
            Объект Frame.
        """
        return self.page.frame(name=frame_id)


class NestedFramesPage(BasePage):
    """Page Object для страницы https://demoqa.com/nestedframes.

    Демонстрирует цепочку frame_locator().frame_locator() для работы
    с вложенными iframe — распространённый сценарий в legacy enterprise UI.
    """

    PARENT_FRAME = "#frame1"
    CHILD_FRAME = "iframe"
    PARENT_BODY_TEXT = "body"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "NestedFramesPage":
        """Открыть страницу Nested Frames."""
        super().open("/nestedframes")
        return self

    def get_parent_frame_text(self) -> str:
        """Получить текст body родительского фрейма.

        Returns:
            Текстовое содержимое body в parent frame.
        """
        locator = self.page.frame_locator(self.PARENT_FRAME).locator(self.PARENT_BODY_TEXT)
        return locator.text_content() or ""

    def get_child_frame_text(self) -> str:
        """Получить текст body дочернего фрейма через цепочку frame_locator.

        Returns:
            Текстовое содержимое body в child frame внутри parent frame.
        """
        locator = (
            self.page.frame_locator(self.PARENT_FRAME)
            .frame_locator(self.CHILD_FRAME)
            .locator(self.PARENT_BODY_TEXT)
        )
        return locator.text_content() or ""
