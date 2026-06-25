import json
from pathlib import Path
from django.shortcuts import render, redirect

DATA_PATH = Path(__file__).resolve().parent.parent.parent / 'data.json'

def get_data():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

SECTIONS = [
    'about', 'goal', 'journey', 'mentor',
    'progress', 'hobbies', 'works', 'github'
]

SECTION_NAMES = [
    'О себе', 'Моя цель', 'Как пришёл в IT', 'Ментор',
    'Точка А→Б', 'Хобби', 'Мои работы', 'GitHub'
]

def index(request):
    menu = list(zip(SECTIONS, SECTION_NAMES))
    return render(request, 'portfolio/index.html', {'menu': menu})

def section(request, slug):
    if slug not in SECTIONS:
        return redirect('index')
    data = get_data()
    idx = SECTIONS.index(slug)
    menu = list(zip(SECTIONS, SECTION_NAMES))
    return render(request, 'portfolio/section.html', {
        'slug': slug,
        'title': SECTION_NAMES[idx],
        'data': data,
        'menu': menu,
    })
