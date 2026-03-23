"""Вспомогательные утилиты."""

import random
import time
from typing import Any, Callable


def wait_for(
    condition: Callable[[], bool],
    timeout: int = 10,
    poll_frequency: float = 0.5,
) -> bool:
    """Ожидать выполнения условия с polling.

    Args:
        condition: Функция, возвращающая bool.
        timeout: Максимальное время ожидания (сек).
        poll_frequency: Частота проверки (сек).

    Returns:
        True если условие выполнено в пределах таймаута, иначе False.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if condition():
            return True
        time.sleep(poll_frequency)
    return False


def generate_random_email() -> str:
    """Сгенерировать случайный email.

    Returns:
        Строка с email-адресом.
    """
    domains = ["example.com", "test.com", "demo.com"]
    return f"user{random.randint(1000, 9999)}@{random.choice(domains)}"


def retry_on_failure(max_retries: int = 3, delay: float = 1.0) -> Callable:
    """Декоратор для повторного выполнения при ошибке.

    Args:
        max_retries: Максимальное количество попыток.
        delay: Базовая задержка между попытками (сек).

    Returns:
        Декоратор функции.
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay * (attempt + 1))
            raise last_exception
        return wrapper
    return decorator


def highlight_element(page: Any, locator: Any) -> None:
    """Подсветить элемент красной рамкой (для отладки).

    Args:
        page: Объект страницы Playwright.
        locator: Локатор элемента.
    """
    locator.evaluate("element => element.style.border = '3px solid red'")
