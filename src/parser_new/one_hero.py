import requests
from bs4 import BeautifulSoup
import re

def clean_next(text):
    return re.sub(r'\s+', ' ', text)

def get_hero_info(lang, name_hero_en):
    url = f"https://raid.guide/{lang}/shadow-legends/{name_hero_en}/"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"[{lang}] Не вдалося отримати {name_hero_en}: {response.status_code}")
        return {}

    soup = BeautifulSoup(response.content, 'html.parser')
    name_hero = soup.find('h1').get_text()
    details_div = soup.find('div', class_='champion-details')
    if not details_div:
        return {}

    table_links = details_div.find('table', class_='table').find_all('a')
    characteristics = [link.get_text() for link in table_links]
    aura_section = soup.find('section', class_='champion-aura')
    aura = (clean_next(aura_section.find('p').get_text())
            .replace(' %', '%.').replace(':', ': ')) if aura_section else None

    skills_section = soup.find('section', class_='champion-skills')
    skills = {}
    for i, skill_div in enumerate(skills_section.find_all('div', class_='skill')):
        name = skill_div.find('h4').get_text()
        img = skill_div.find('picture')
        img_url = 'https://raid.guide' + img.get('data-iesrc') if img else None
        formulas = {f'formula_{j+1}': clean_next(f.get_text())
                    for j, f in enumerate(skill_div.find_all('div', class_='skill-formula'))}
        text = clean_next(skill_div.find('article').get_text())
        tds = skill_div.find_all('td')
        levels = {}
        j = 0
        for k in range(0, len(tds), 3):
            if k + 1 < len(tds):
                j += 1
                levels[j] = {
                    'type': clean_next(tds[k+1].get_text()),
                    'amount': clean_next(tds[k+2].get_text()).replace(' %', '%')
                }
        skills[f'skill_{i+1}'] = {
            'name': name,
            'skill_img_url': img_url,
            'formula': formulas,
            'text': text,
            'skill_levels': levels
        }

    stats_section = soup.find('section', class_='pt-5')
    keys = [th.get_text() for th in stats_section.find_all('th')]
    vals = [clean_next(td.get_text()).strip() for td in stats_section.find_all('td')]
    stats = {k: v for k, v in zip(keys, vals)}

    return {
        'name': name_hero,
        'characteristics': {
            'fraction_hero': characteristics[0] if len(characteristics) > 0 else '',
            'elements_hero': characteristics[1] if len(characteristics) > 1 else '',
            'type_hero': characteristics[2] if len(characteristics) > 2 else '',
            'rarity_hero': characteristics[3] if len(characteristics) > 3 else ''
        },
        'aura': aura,
        'skills': skills,
        'stats_by_level': stats
    }

def get_hero_info_lang(name_hero_en):
    langs = ['en', 'uk', 'ru']  # можна змінити на ['en', 'uk', 'ru'] для повної обробки
    # heroes_info = {}
    # for lang in langs:
    #     heroes_info[lang] = get_hero_info(lang, name_hero_en)
    return {lang: get_hero_info(lang, name_hero_en) for lang in langs}

