"""Точка входа для запуска тестов DemoQA."""

import subprocess
import sys


def run_tests(
    markers: str = "",
    headless: bool = True,
    report: bool = True,
) -> int:
    """Запустить тесты с заданными параметрами.

    Args:
        markers: Маркер pytest (smoke, regression, ui).
        headless: Режим без GUI.
        report: Генерировать HTML-отчёт.

    Returns:
        Код завершения процесса.
    """
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/",
        "-v",
    ]

    if markers:
        cmd.extend(["-m", markers])

    if report:
        cmd.extend(
            [
                "--html=reports/html/report.html",
                "--self-contained-html",
            ]
        )

    env_vars = {}
    if headless:
        env_vars["HEADLESS"] = "true"
    else:
        env_vars["HEADLESS"] = "false"

    print(f"Запуск тестов: {' '.join(cmd)}")
    result = subprocess.run(cmd, env={**__import__("os").environ, **env_vars})
    return result.returncode


if __name__ == "__main__":
    print("=" * 60)
    print("  DemoQA Automation Framework")
    print("=" * 60)

    print("\nЗапуск Smoke-тестов...")
    exit_code = run_tests(markers="smoke", headless=True)

    sys.exit(exit_code)
