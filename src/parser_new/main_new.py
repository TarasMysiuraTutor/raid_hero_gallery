import json
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import uuid
# from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor
import time

# Основна сторінка зі списком героїв
url_main = "https://raid.guru/en/heroes/"

# Функція для очищення тексту від небажаних символів
def clean_text(text):
    """Очищення тексту від символів типу &ZeroWidthSpace та пробілів."""
    if isinstance(text, str):  # '\u200b'
        # text.replace("\u200b", "").strip()
        return text.replace("\u200b", "").replace("&ZeroWidthSpace;", "").strip()
    return text

# Функція для отримання посилань на героїв зі сторінки
def get_hero_links_from_page(url):
    """Парсинг сторінки для отримання посилань на героїв."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            hero_cards = soup.select(".image > a")  # Витягуємо картки героїв

            data_heroes = []
            for card in hero_cards:
                hero_data = {}
                image_element = card.select_one("a > img")
                if image_element:
                    hero_data["hero_name"] = clean_text(image_element.get("title", "Title not found"))
                    hero_data["image_url"] = clean_text(image_element.get("src", "URL not found"))
                if card:
                    hero_data["hero_url"] = clean_text(card.get("href", "URL not found"))
                    data_heroes.append(hero_data)
            return data_heroes
        else:
            print(f"Page load failed, status code: {response.status_code}")
    except requests.HTTPError as http_err:
        print(f"HTTP error: {http_err}")
    except Exception as err:
        print(f"Other error: {err}")

# Функція для перебору сторінок з пагінацією
def scrape_to_links_all_pages(url_en):
    """Скрапінг усіх сторінок з пагінацією."""
    page = 1
    all_data = []
    while True:
        page_url = f"{url_en}?page={page}"
        print(f"Scraping page {page}...")
        data = get_hero_links_from_page(page_url)
        if not data:
            break
        all_data.extend(data)

        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, "html.parser")
        next_button = soup.select_one(".pagination > li > a")
        if next_button:
            page += 1
        else:
            break
    return all_data


# Функція для витягування деталей героя
def extract_data(url):
    """Отримання даних про героя (зображення, опції, опис)."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Витягуємо інформацію про зображення
        image_data = {}
        link_element = soup.find(class_="main-image")
        if link_element:
            image_element = link_element.select_one("img")
            image_data["title"] = clean_text(image_element.get("title", "Title not found"))
            image_data["url_large"] = clean_text(link_element.get("href", "URL not found"))
            image_data["url_small"] = clean_text(image_element.get("src", "Title not found"))

        # Витягуємо опції героя
        text_elements = soup.select_one(".row .col-sm-12.col-md-7.product_informationss .list-unstyled")
        texts = {}
        if text_elements:
            for element in text_elements:
                text_data = element.get_text(strip=True)
                parts = text_data.split(":")
                if len(parts) == 2:
                    key, value = parts
                    if key == "Бафы":
                        key = "Buffs"
                    if key == "Навыки":
                        key = "Skills"
                    if key.lower() in ["critical chance", "critecal chance", "cretical chance", "cretecal chance",
                                       "crite chance", "crite. chance", "crit. chance", "crete chance", "crete. chance",
                                       "cret. chance", "критический шанс", "крит. шанс"]:
                        value = "15 %"
                        # Видалення порожніх ключів і значень
                    if value not in ["", None, '', {}, []]:
                        texts[clean_text(key)] = (clean_text(value))

        # Витягуємо опис героя
        description_elements = soup.find(id="tab-description")

        data_dict = {}
        b_tags = description_elements.find_all("b")

        for b_tag in b_tags:
            # Отримуємо текст з тегу <b>
            key = clean_text(b_tag.get_text(strip=True))

            # Наступний братній елемент після <b> (може бути <br> або текст)
            value = ""
            next_sibling = b_tag.next_sibling

            while next_sibling:
                if next_sibling.name == "b":
                    break
                if next_sibling.name == "br":
                    value += "\n"
                elif next_sibling.string:
                    value += next_sibling.string.strip() + " "
                next_sibling = next_sibling.next_sibling

            # Зберігаємо значення у словник
            if "PVE" not in key:
                if "PVP" not in key:
                    if value not in ["", None, '', {}, []]:
                        data_dict[key] = clean_text(value.strip())


            # data_dict[key] = clean_text(value.strip())

        h3_tags = description_elements.find_all("h3")

        for h3_tag in h3_tags:
            # Отримуємо текст з тегу <b>
            key = clean_text(h3_tag.get_text(strip=True))

            # Наступний братній елемент після <b> (може бути <br> або текст)
            value = ""
            next_sibling = h3_tag.next_sibling

            while next_sibling:
                if next_sibling.name == "b":
                    break
                if next_sibling.name == "br":
                    value += "\n"
                elif next_sibling.string:
                    value += next_sibling.string.strip() + " "
                next_sibling = next_sibling.next_sibling

            # Зберігаємо значення у словник
            if "PVE" not in key:
                if "PVP" not in key:
                    if value not in ["", None, '', {}, []]:
                        data_dict[key] = clean_text(value.strip())

            # data_dict[key] = value.strip()

        return [image_data, texts, data_dict]
    except requests.HTTPError as http_err:
        print(f"HTTP error: {http_err}")
    except Exception as err:
        print(f"Other error: {err}")


# Функція для обробки всіх посилань
def extends_Dataset(data_links):
    """Створення фінального датасету для всіх героїв."""

    def process_link(link_data):
        hero_id = str(uuid.uuid4())
        link = link_data["hero_url"]
        hero_name = link_data["hero_name"]
        print(f"Processing Hero: ID={hero_id}, Name={hero_name} ({data_links.index(link_data) + 1}/{len(data_links)})")
        data_en = extract_data(link)
        url_ru = link.replace("/en/", "/")
        data_ru = extract_data(url_ru)
        return {
            "id": hero_id,
            "en": {
                "hero_name": data_en[0]["title"].split(" - ")[0],
                "image_large_url": data_en[0]["url_large"],
                "image_small_url": data_en[0]["url_small"],
                "options": data_en[1],
                "description": data_en[2],
            },
            "ru": {
                "hero_name": data_ru[0]["title"].split(" (")[0],
                "image_large_url": data_ru[0]["url_large"],
                "image_small_url": data_ru[0]["url_small"],
                "options": data_ru[1],
                "description": data_ru[2],
            },
        }

    # Використовуємо багатопотоковість для пришвидшення обробки
    with ThreadPoolExecutor(max_workers=10) as executor:
        dataset = list(executor.map(process_link, data_links))
    return dataset


# Збереження результатів у JSON
def save_to_json(data):
    """Фільтрація даних і збереження у JSON."""
    data = [
        {k: v for k, v in hero.items() if v} for hero in data
    ]
    with open("hero_data_optimized.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print("Data saved to hero_data_optimized.json")


# Основна програма
if __name__ == "__main__":
    start_time = time.time()
    data_links = scrape_to_links_all_pages(url_main)
    dataset = extends_Dataset(data_links)
    save_to_json(dataset)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")
