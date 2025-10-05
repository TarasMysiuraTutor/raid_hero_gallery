from itertools import count
import requests
from bs4 import BeautifulSoup
import json
import one_hero
from concurrent.futures import ThreadPoolExecutor, as_completed
import time  # додай на початку файлу
import os
from pymongo import MongoClient
import sys
import io

MONGO_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = "raid_db_new"
COLLECTION_NAME = "heroes"

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "parsed_data")

def save_to_json_split(data, base_filename='parser/parsed_data/heroes_part', count_part=7):
    if not data:
        print("⚠️ Список героїв порожній. Немає чого зберігати.")
        return

    # Створення папки, якщо не існує
    os.makedirs('parser/parsed_data', exist_ok=True)

    # Збереження повного JSON
    full_filename = 'parser/parsed_data/heroes_all.json'
    with open(full_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"✅ Збережено {len(data)} героїв у файл {full_filename}")

    # Обчислення розміру частин
    chunk_size = len(data) // count_part + (len(data) % count_part > 0)

    # Збереження частинами
    for i in range(count_part):
        start = i * chunk_size
        end = (i + 1) * chunk_size
        if start >= len(data):
            break

        part = data[start:end]
        filename = f"{base_filename}_{i + 1}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(part, f, ensure_ascii=False, indent=4)
        print(f"✅ Збережено {len(part)} героїв у файл {filename}")


def convert_keys_to_str(obj):
    if isinstance(obj, dict):
        return {str(k): convert_keys_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_keys_to_str(elem) for elem in obj]
    else:
        return obj


# 🧩 Збереження у MongoDB
def save_to_mongodb(data, uri=MONGO_URI, db_name=DB_NAME, collection_name=COLLECTION_NAME):
    try:
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]

        collection.delete_many({})
        data_cleaned = [convert_keys_to_str(doc) for doc in data]
        collection.insert_many(data_cleaned)

        print(f"✅ Успішно збережено {len(data_cleaned)} записів у MongoDB ({db_name}.{collection_name})")
    except Exception as e:
        print(f"❌ Помилка при збереженні в MongoDB: {e}")


def get_hero_basic_info(hero_tag):
    hero_name = hero_tag.find('h2', class_='woocommerce-loop-product__title').text.strip()
    name = hero_name
    hero_url = hero_tag.find('a', class_='woocommerce-LoopProduct-link').get('href')
    name_en=hero_url.split('/')[4]
    img_card_url = hero_tag.find('img').get('src')
    return name_en, name, img_card_url, hero_url


def get_full_hero_info(hero_tag):
    name_en, name, img_card_url, hero_url = get_hero_basic_info(hero_tag)
    hero_details = one_hero.get_hero_info_lang(hero_url)  # Отримуємо інфо одразу по всіх мовах
    return {
        'name_en': name_en.title(),
        'name': name,
        'img': img_card_url,
        'url': hero_url,        
        'details': hero_details
    }


def get_heroes_info():
    URL = "https://raid-sl.ru/heroes-tag/bannerety"
    response = requests.get(URL)
    if response.status_code != 200:
        print(f"Не вдалося отримати сторінку. Код стану: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    heroes_info_all=soup.find_all('li', class_='product')
    # heroes = soup.find_all('a', class_='woocommerce-LoopProduct-link')
    
    print(f"Знайдено {len(heroes_info_all)} героїв")

    heroes_info = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        count_heroes = len(heroes_info_all)
        # count_heroes=4
        futures = [executor.submit(get_full_hero_info, heroes_info_all[hero_index]) for hero_index in range(count_heroes)]
        for i, future in enumerate(as_completed(futures), 1):
            try:
                hero_data = future.result()
                print(f"{i} із {len(heroes_info_all)} оброблено: {hero_data['name']}")
                heroes_info.append(hero_data)
            except Exception as e:
                print(f"Помилка при обробці героя: {e}")
    return heroes_info

def main():
    start_time = time.time()
    heroes_info = get_heroes_info()
    save_to_json_split(heroes_info)
    # save_to_mongodb(heroes_info)
    end_time = time.time()
    elapsed = end_time - start_time
    if elapsed // 60 == 1:
        minutes = 'хвилина'
    elif elapsed // 60 == 2 or elapsed // 60 == 3:
        minutes = 'хвилини'
    else:
        minutes = 'хвилин'
    print(f"\n[TIME] Парсинг завершено Обробка завершена за {int(elapsed // 60)} {minutes} {elapsed % 60:.2f} секунд.")


if __name__ == "__main__":
    main()
