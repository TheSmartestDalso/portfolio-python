import json
import re


def load_data(path: str = "data.json") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)



def divider(char: str = "─", width: int = 54) -> str:
    return char * width


def box_title(text: str, width: int = 54) -> str:
    inner = width - 2
    line_top    = "╔" + "═" * inner + "╗"
    line_bottom = "╚" + "═" * inner + "╝"
    line_text   = "║" + text.center(inner) + "║"
    return f"\n{line_top}\n{line_text}\n{line_bottom}"


def bullet(text: str, symbol: str = "▸") -> str:
    return f"  {symbol} {text}"


def label(key: str, value: str) -> str:
    return f"  {key}: {value}"



class Portfolio:
    def __init__(self, data_path: str = "data.json"):
        self._data = load_data(data_path)

    def show_about(self) -> None:
        d = self._data["about"]
        print(box_title("★  О СЕБЕ"))
        print(label("Имя",       d["name"]))
        print(label("Возраст",   f"{d['age']} лет"))
        print(label("Роль",      d["role"]))
        print(f"\n{divider()}")
        print("  Факты обо мне:")
        for fact in d["facts"]:
            print(bullet(fact))

    def show_goal(self) -> None:
        d = self._data["goal"]
        print(box_title("◎  МОЯ ЦЕЛЬ"))
        print(bullet(d["short"]))
        print()
        print("  В долгосрочных планах:")
        print(bullet(d["long"]))

    def show_journey(self) -> None:
        steps = self._data["journey"]
        print(box_title("  КАК Я ПРИШЁЛ В IT"))
        for i, step in enumerate(steps, start=1):
            print(f"  {i}. {step}")

    def show_mentor(self) -> None:
        d = self._data["mentor"]
        print(box_title("  МОЙ МЕНТОР"))
        print(label("Имя", d["name"]))
        print(f"\n  Чему научил:")
        for item in d["contributions"]:
            print(bullet(item))

    def show_progress(self) -> None:
        d = self._data["progress"]
        print(box_title("  ТОЧКА А  →  ТОЧКА Б"))
        print(f"  {'Было':^24} │ {'Стало':^24}")
        print(f"  {divider('-', 24)} │ {divider('-', 24)}")
        max_len = max(len(d["point_a"]), len(d["point_b"]))
        for i in range(max_len):
            a = d["point_a"][i] if i < len(d["point_a"]) else ""
            b = d["point_b"][i] if i < len(d["point_b"]) else ""
            print(f"  {('✗ ' + a)[:24]:<24} │ {'✓ ' + b}")

    def show_hobbies(self) -> None:
        hobbies = self._data["hobbies"]
        print(box_title("  ХОББИ И ИНТЕРЕСЫ"))
        for hobby in hobbies:
            print(bullet(hobby))

    def show_works(self) -> None:
        works = self._data["works"]
        print(box_title("🏆  МОИ ЛУЧШИЕ РАБОТЫ"))
        for i, work in enumerate(works, start=1):
            print(f"\n  [{i}] {work['title']}")
            print(f"      {work['description']}")
            print(f"       {work['link']}")

    def show_github(self) -> None:
        link = self._data["github"]
        print(box_title("  МОЙ GITHUB"))
        print(bullet(f"Профиль: {link}", "→"))
        print()
        print(bullet("Проект портфолио: portfolio-python", "📁"))

    SECTIONS: dict = {
        "1": ("О себе",              "show_about"),
        "2": ("Моя цель",            "show_goal"),
        "3": ("Как я пришёл в IT",   "show_journey"),
        "4": ("Мой ментор",          "show_mentor"),
        "5": ("Точка А → Точка Б",   "show_progress"),
        "6": ("Хобби и интересы",    "show_hobbies"),
        "7": ("Мои лучшие работы",   "show_works"),
        "8": ("GitHub",              "show_github"),
    }

    def show_section(self, key: str) -> bool:
        entry = self.SECTIONS.get(key)
        if not entry:
            return False
        method = getattr(self, entry[1])
        print()
        method()
        print(f"\n{divider()}")
        return True



VALID_INPUT_RE = re.compile(r"^[0-8]$")


def validate_choice(raw: str) -> str | None:
    cleaned = raw.strip()
    if VALID_INPUT_RE.match(cleaned):
        return cleaned
    return None