import pygame
import json
import sys

pygame.init()

WIDTH = 900
HEIGHT = 620
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Портфолио")
clock = pygame.time.Clock()

BG = (20, 20, 28)
BLUE = (100, 160, 255)
WHITE = (210, 210, 220)
GRAY = (110, 110, 130)
CUBE = (35, 35, 50)

font_big = pygame.font.SysFont("segoeui", 32, bold=True)
font_med = pygame.font.SysFont("segoeui", 15)
font_sm = pygame.font.SysFont("segoeui", 13)

import os as _os
_DATA_PATH = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "data.json")
with open(_DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

current = None

menu_items = ["О себе", "Моя цель", "Как пришёл в IT", "Ментор",
              "Точка А->Б", "Хобби", "Мои работы", "GitHub"]


def draw_text_wrapped(text, font, color, x, y, max_w):
    words = text.split()
    line = ""
    for word in words:
        test = line + " " + word if line else word
        if font.size(test)[0] <= max_w:
            line = test
        else:
            screen.blit(font.render(line, True, color), (x, y))
            y += font.get_height() + 3
            line = word
    if line:
        screen.blit(font.render(line, True, color), (x, y))
        y += font.get_height() + 3
    return y


def draw_home():
    title = font_big.render("Портфолио", True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 80)))

    sub = font_med.render("Атығай Дамир  -  Python / Django / Gamedev", True, GRAY)
    screen.blit(sub, sub.get_rect(center=(WIDTH // 2, 120)))

    cube_w = 180
    cube_h = 90
    cols = 4
    gap_x = 20
    gap_y = 16
    start_x = (WIDTH - (cols * cube_w + (cols - 1) * gap_x)) // 2
    start_y = 200

    for i, name in enumerate(menu_items):
        col = i % cols
        row = i // cols
        x = start_x + col * (cube_w + gap_x)
        y = start_y + row * (cube_h + gap_y)

        pygame.draw.rect(screen, CUBE, (x, y, cube_w, cube_h), border_radius=8)
        pygame.draw.rect(screen, BLUE, (x, y, cube_w, cube_h), 1, border_radius=8)

        num = font_med.render(str(i + 1), True, BLUE)
        screen.blit(num, (x + 10, y + 8))

        label = font_med.render(name, True, WHITE)
        screen.blit(label, label.get_rect(center=(x + cube_w // 2, y + cube_h // 2 + 6)))

    hint = font_sm.render("Нажми 1–8 чтобы открыть раздел", True, GRAY)
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 490)))


def draw_section(idx):
    back = font_sm.render("← ESC  назад", True, GRAY)
    screen.blit(back, (20, 18))

    title = font_med.render(f"{idx + 1}. {menu_items[idx]}", True, BLUE)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 22)))

    x, y = 60, 60

    if idx == 0:
        screen.blit(font_med.render(data["about"]["name"], True, WHITE), (x, y)); y += 24
        screen.blit(font_med.render(data["about"]["role"], True, GRAY), (x, y)); y += 22
        screen.blit(font_med.render(f"{data['about']['age']} лет", True, GRAY), (x, y)); y += 30
        for fact in data["about"]["facts"]:
            y = draw_text_wrapped("- " + fact, font_sm, WHITE, x, y, 780); y += 4

    elif idx == 1:
        y = draw_text_wrapped(data["goal"]["short"], font_med, WHITE, x, y, 780); y += 16
        y = draw_text_wrapped(data["goal"]["long"], font_sm, GRAY, x, y, 780)

    elif idx == 2:
        for i, step in enumerate(data["journey"]):
            y = draw_text_wrapped(f"{i+1}. {step}", font_med, WHITE, x, y, 780); y += 8

    elif idx == 3:
        screen.blit(font_med.render(data["mentor"]["name"], True, WHITE), (x, y)); y += 26
        for item in data["mentor"]["contributions"]:
            y = draw_text_wrapped("- " + item, font_med, WHITE, x, y, 780); y += 6

    elif idx == 4:
        screen.blit(font_sm.render("Было:", True, GRAY), (x, y)); y += 20
        for item in data["progress"]["point_a"]:
            screen.blit(font_sm.render("- " + item, True, GRAY), (x + 10, y)); y += 18
        y += 10
        screen.blit(font_sm.render("Стало:", True, BLUE), (x, y)); y += 20
        for item in data["progress"]["point_b"]:
            screen.blit(font_sm.render("- " + item, True, WHITE), (x + 10, y)); y += 18

    elif idx == 5:
        for hobby in data["hobbies"]:
            y = draw_text_wrapped("- " + hobby, font_med, WHITE, x, y, 780); y += 6

    elif idx == 6:
        for i, work in enumerate(data["works"]):
            screen.blit(font_med.render(f"{i+1}. {work['title']}", True, BLUE), (x, y)); y += 20
            y = draw_text_wrapped(work["description"], font_sm, GRAY, x + 14, y, 766); y += 14

    elif idx == 7:
        screen.blit(font_med.render(data["github"], True, BLUE), (x, y)); y += 26
        screen.blit(font_sm.render("Репо: portfolio-python", True, GRAY), (x, y))


while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                current = None
            key_map = {
                pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3,
                pygame.K_5: 4, pygame.K_6: 5, pygame.K_7: 6, pygame.K_8: 7
            }
            if event.key in key_map:
                current = key_map[event.key]

    screen.fill(BG)

    if current is None:
        draw_home()
    else:
        draw_section(current)

    pygame.display.flip()