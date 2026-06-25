import sys
import os
from portfolio import Portfolio, validate_choice

# ─── sys.argv: опциональный путь к data.json ─────────────────────────────────
# Запуск: python main.py           — ищет data.json рядом
#         python main.py path/to/data.json  — указываешь путь явно
if len(sys.argv) >= 2:
    data_path = sys.argv[1]
else:
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data.json")

try:
    portfolio = Portfolio(data_path)
except FileNotFoundError:
    print(f"Ошибка: файл не найден — {data_path}")
    print("Использование: python main.py [путь/к/data.json]")
    sys.exit(1)
except Exception as e:
    print(f"Ошибка загрузки данных: {e}")
    sys.exit(1)

print("\n=== ПОРТФОЛИО ===")
print("Атығай Дамир | Python / Django / Gamedev\n")

while True:
    print("Меню:")
    for key, (title, _) in portfolio.SECTIONS.items():
        print(f"  {key}. {title}")
    print("  0. Выход")

    try:
        raw = input("\nВведи номер: ")
    except (KeyboardInterrupt, EOFError):
        print("\n\nПока! github.com/TheSmartestDalso")
        break

    choice = validate_choice(raw)

    if choice is None:
        print("Неверный ввод — введи цифру от 0 до 8\n")
        continue

    if choice == "0":
        print("\nПока! github.com/TheSmartestDalso")
        break

    portfolio.show_section(choice)
    print()
