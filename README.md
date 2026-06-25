# 🤖 Портфолио — Атығай Дамир

Привет, я делал это портфолио более 20 часов, надеюсь оно будет достойным.

Портфолио реализовано в **4 версиях**: Telegram-бот, Django-сайт, Pygame-приложение и терминал.
Все версии берут данные из одного файла `data.json` в корне проекта.

## 🚀 Быстрый старт

Сначала установи все зависимости:
```bash
pip install -r requirements.txt
```

Затем заполни `data.json` в корне — вставь свои токены вместо `YOUR_TELEGRAM_TOKEN` и `YOUR_OPENROUTER_TOKEN`.

---

## 📁 Структура проекта

```
portfolio-python/
├── data.json              ← общий файл данных для всех версий
├── requirements.txt
├── README.md
├── portfolio_Telebot/     ← Telegram-бот
├── portfolio_django/      ← Django-сайт
├── portfolio_pygame/      ← Pygame-приложение
└── portfolio_terminal/    ← Терминальная версия
```

---

## 🗂 Разделы портфолио (8 блоков)

| # | Раздел |
|---|--------|
| 1 | О себе |
| 2 | Моя цель |
| 3 | Как пришёл в IT |
| 4 | Ментор |
| 5 | Точка А → Б |
| 6 | Хобби и интересы |
| 7 | Мои лучшие работы |
| 8 | GitHub |

---

## 1. 🖥 ТЕРМИНАЛ (portfolio_terminal)

```bash
cd portfolio_terminal
python main.py
```

- Вводи цифры `1–8` чтобы открыть раздел
- `0` — выход

Можно указать путь к data.json явно:
```bash
python main.py ../data.json
```

---

## 2. 🎮 PYGAME (portfolio_pygame)

```bash
cd portfolio_pygame
python portfolio_gui.py
```

- Нажимай `1–8` на клавиатуре или кликай по кубам
- `ESC` — вернуться назад

---

## 3. 🌐 DJANGO (portfolio_django)

```bash
cd portfolio_django
python manage.py runserver
```

Открой браузер: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Кликай по карточкам для навигации по разделам.

---

## 4. 🤖 TELEGRAM БОТ (portfolio_Telebot)

```bash
cd portfolio_Telebot
python Bot.py
```

Найди бота в Telegram: [@ADDs_portfolio_bot](https://t.me/ADDs_portfolio_bot)

Напиши `/start` и выбирай разделы кнопками или командами:

| Команда | Раздел |
|---------|--------|
| `/about` | О себе |
| `/goal` | Моя цель |
| `/journey` | Как пришёл в IT |
| `/mentor` | Ментор |
| `/progress` | Точка А → Б |
| `/hobbies` | Хобби |
| `/works` | Мои работы |
| `/github` | GitHub |
| `/ask <вопрос>` | Задать вопрос ИИ |

Или напиши `вопрос: <твой вопрос>` — ответит ИИ на основе данных портфолио.

Запуск с аргументами командной строки:
```bash
python Bot.py <TELEGRAM_TOKEN> <OPENROUTER_TOKEN> --debug
```

---

## 🔗 Ссылки

- **GitHub:** https://github.com/TheSmartestDalso/portfolio-python
- **Telegram-бот:** https://t.me/ADDs_portfolio_bot
