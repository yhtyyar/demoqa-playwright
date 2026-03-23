"""Главная страница DemoQA."""

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class MainPage(BasePage):
    """Page Object для главной страницы https://demoqa.com/."""

    # --- Локаторы: главное меню ---
    CARD_ELEMENTS = ".category-cards .card:nth-child(1)"
    CARD_FORMS = ".category-cards .card:nth-child(2)"
    CARD_ALERTS = ".category-cards .card:nth-child(3)"
    CARD_WIDGETS = ".category-cards .card:nth-child(4)"
    CARD_INTERACTIONS = ".category-cards .card:nth-child(5)"
    CARD_BOOKSTORE = ".category-cards .card:nth-child(6)"

    # --- Локаторы: боковое меню Elements ---
    MENU_ITEM_TEXTBOX = "li#item-0 span:has-text('Text Box')"
    MENU_ITEM_CHECKBOX = "li#item-1 span:has-text('Check Box')"
    MENU_ITEM_RADIO = "li#item-2 span:has-text('Radio Button')"
    MENU_ITEM_TABLES = "li#item-3 span:has-text('Web Tables')"
    MENU_ITEM_BUTTONS = "li#item-4 span:has-text('Buttons')"
    MENU_ITEM_LINKS = "li#item-5 span:has-text('Links')"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "MainPage":
        """Открыть главную страницу."""
        super().open("/")
        return self

    # --- Свойства ---

    @property
    def elements_card(self) -> Locator:
        """Карточка раздела Elements."""
        return self.page.locator(self.CARD_ELEMENTS)

    @property
    def forms_card(self) -> Locator:
        """Карточка раздела Forms."""
        return self.page.locator(self.CARD_FORMS)

    # --- Навигация ---

    def go_to_textbox(self) -> "MainPage":
        """Перейти на страницу TextBox через меню."""
        self.click(self.elements_card)
        self.click(self.page.locator(self.MENU_ITEM_TEXTBOX))
        return self

    def go_to_checkbox(self) -> "MainPage":
        """Перейти на страницу CheckBox через меню."""
        self.click(self.elements_card)
        self.click(self.page.locator(self.MENU_ITEM_CHECKBOX))
        return self

    def go_to_radio(self) -> "MainPage":
        """Перейти на страницу RadioButton через меню."""
        self.click(self.elements_card)
        self.click(self.page.locator(self.MENU_ITEM_RADIO))
        return self

    def go_to_tables(self) -> "MainPage":
        """Перейти на страницу Web Tables через меню."""
        self.click(self.elements_card)
        self.click(self.page.locator(self.MENU_ITEM_TABLES))
        return self

    def go_to_buttons(self) -> "MainPage":
        """Перейти на страницу Buttons через меню."""
        self.click(self.elements_card)
        self.click(self.page.locator(self.MENU_ITEM_BUTTONS))
        return self

    def go_to_links(self) -> "MainPage":
        """Перейти на страницу Links через меню."""
        self.click(self.elements_card)
        self.click(self.page.locator(self.MENU_ITEM_LINKS))
        return self
