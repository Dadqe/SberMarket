import pprint
import sys
import os
import json
from pathlib import Path
from typing import Any
import requests
import time
from selenium import webdriver
import pickle
from random import uniform

# Добавляю в поиск путей корневую директорию всех файлов
sys.path.insert(1, os.getcwd())
from sbermarket_api.client import Client
from sbermarket_api.store import Store

PYTHON_PATH = Path(__file__)                    # Объект пути к исполняемому питоновскому файлу
DIR_MYWORK = PYTHON_PATH.parent                 # Путь, где расположен скрипт, который запускается
DATA_PATH = DIR_MYWORK / 'Data'                 # Путь, где хранятся данные, получаемые при работе скрипта. Задумывается, что в той же директории (рядом с файлом питона, который запускается) создаётся папка Data и там сохраняется всё под своими именами
MY_COORDS = {'lat': 54.92046, 'lon': 73.469722}
BASE_URL = 'https://sbermarket.ru/api/v3/stores/STORE_ID/products'
# URL_SELENIUM = 'https://sbermarket.ru'

# Headers for selenium
headers = {
    'authority': 'sbermarket.ru',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'api-version': '3.0',
    'client-token': '7ba97b6f4049436dab90c789f946ee2f',
    'is-storefront-ssr': 'false',
    'referer': 'https://sbermarket.ru/metro/c/priedlozhieniia/skidki/ovoshchi-frukti-orekhi?sid=152&source=category',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}

def get_all_stores_for_me(coords: dict[str, float]):
    '''Верну список с доступными магазинами для доставки по указанным координатам. В дальнейшем буду иметь доступ к этому списку'''
    client = Client()
    stores = client.stores(coords['lat'], coords['lon'])    # -> list элементами этого списка являются объекты класса Store
    return stores
    # return client.stores(coords['lat'], coords['lon'])

# Take first store for test functional...
# first_store = get_all_stores_for_me(MY_COORDS)[0]

def get_info_about_store(store: Store) -> tuple[Any, ...]:
    '''Получаю "всю" информацию о магазине, который был передан в данный метод.
    Для получения имени магазина (для создания необходимой папки)
    Для получения slug магазина (для формаирования url for selenium)'''
    store_id = store.store_id
    store_name = store.name
    store_slug = Client().store(store_id).__dict__['retailer']['slug']
    return (store_id, store_name, store_slug)

def get_discount_category(store: Store) -> dict:        # Вернётся кортеж с категориями и названием магазина, что б потом создать папку нужную
    '''Получу всеее скидочные категории
    Они будут с избытком информации, в следующей функции я распарсю этот словарь в более удобоваримый вариант.'''
    categories = store.categories()                                 # Получаю все категории, которые есть магазине, который передали в функцию
    only_discount_category = categories['promoted_categories'][0]   # -> dict Вытаскиваю словарь только с обычными скидками (т.к. в первой вложенности есть ещё скидки до 60%)
    return only_discount_category

def parse_discount_category(pre_discount_category: dict) -> dict[str, str]:
    name_url_in_discount_category = {category['name']: category['canonical_url'].replace('https://sbermarket.ru/categories/', '') for category in pre_discount_category['children']}  # Создаю словарь с название категории: url по которому смогу делать запрос и парсить дальше товары из категории. Сразу отрезал от ссылки ненужный префикс, базовый url, т.к. для запроса нужно будет передать в словарь params преобразованную ссылку
    return name_url_in_discount_category

def save_cookies_in_files_from_selenium(store: Store, category_url: str, store_slug: str, store_id: str) -> dict:
    '''Запущу селениум, сделаю запрос на картегорию, нужную мне и сохраню куки в файл рядом с исполняемым файлом. В App V0.1 я это пробую сохранять в экземпляр класса, что б использовать без кучи открытия и записи и чтения файлов'''
    
    url_selenium = f'https://sbermarket.ru/{store_slug}/c/{category_url}?sid={store_id}&source=category'
    print(f"From selenium: {url_selenium}")
    # options
    options = webdriver.ChromeOptions()
    # disable webdriver mode
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    with webdriver.Chrome(executable_path=r"E:\+CODE\Sber (Selenium)\chromedriver\chromedriver.exe", options=options) as driver:
        # Путь драйвера стоило бы переписать. Положить рядом с исполняемым и использовать
        driver.get(url_selenium)
        time.sleep(10)
        # cookies
        # save on PC
        # pickle.dump(driver.get_cookies(), open('cookies', 'wb'))
        
        # work in process
        cookies = driver.get_cookies()
        cookies = {cookie.get('name'): cookie.get('value') for cookie in cookies}  # Сохраняю словарь cookies в словарь, возвращаю, что б можно было потом использовать
        with open('mywork/Tests/cookies.txt', 'w', encoding='utf-8') as f:
            f.write(str(cookies))
        print('[?] Cookies были получены и сохранены')  # INFO
        
        return cookies

def scrap_one_category(store_id: str, name_store: str, category_url: str, category_name: str, cookies: dict, headers: dict = headers, base_url: str = BASE_URL, data_path: Path = DATA_PATH):
    '''Передам ссылку на категорию, куки, которые получил и отправлю requests запрос, что б получить json по товарам...'''
    url_for_request = base_url.replace('STORE_ID', str(store_id))
    # url_for_request = url_for_request[:url_for_request.find('/stores')+1] + "v3" + url_for_request[url_for_request.find('/stores'):]
    page = 1
    print(url_for_request)
    MAGAZIN_PATH = data_path / name_store
    if not MAGAZIN_PATH.exists():
        MAGAZIN_PATH.mkdir(parents=True, exist_ok=True)
    
    params = {
    'tid': category_url,
    'page': str(page),
    'per_page': '20',
    'sort': 'popularity',
    }
    
    response_first_page = requests.get(url_for_request, params=params, cookies=cookies, headers=headers, timeout=10)
    if response_first_page.status_code == 200:
        total_pages = response_first_page.json()['meta']['total_pages']
    
        list_of_products = response_first_page.json()['products']
        time.sleep(1)
        if total_pages > 1:
            for i in range(2, total_pages+1):
                cur_page = i
                params.update({'page': str(cur_page)})
                response = requests.get(url_for_request, params=params, cookies=cookies, headers=headers)
                list_of_products.extend(response.json()['products'])
                time.sleep(uniform(0.8, 1.5))
        
        with open(MAGAZIN_PATH / f'{category_name}.json', 'w', encoding='utf-8') as f:
            json.dump(list_of_products, f, indent=4, ensure_ascii=False)
    else:
        with open('crash.html', 'w', encoding='utf-8') as f:
            f.write(response_first_page.text)
        print(f"[INFO] Не получилось получить нормальный ответ...")
        print(f"From scraP: {url_for_request}")
    
    # Надо создать отдельную функцию, которая будет посылать запрос и возвращать товары, что б её тут использовать. Я узнаю, сколько всего страниц и один раз использую эту функцию, что б получить товары с первой страницы, а потом пройтись по оставшимся

def parse_category(name_store: str, category_name: str, data_path: Path = DATA_PATH):
    MAGAZIN_PATH = data_path / name_store
    
    with open(MAGAZIN_PATH / f'{category_name}.json', 'r', encoding='utf-8') as f:
        data = json.load(f) # Получаю list с dict один dict == одному товару
    
    necessary_data = []
    for product in data:
        name = product['name']
        price = product['price']
        discount_percent = int((1 - (price / product["original_price"])) * 100)
        necessary_data.append({'name': name, 'price': price, 'discount_percent': discount_percent})
    
    # Отсортирую словарики в списке по значениям ключа 'discount_percent'
    necessary_data = sorted(necessary_data, key=lambda product: product['discount_percent'], reverse=True)
    
    with open(MAGAZIN_PATH / f'{category_name}_clear.json', 'w', encoding='utf-8') as f:
        json.dump(necessary_data, f, indent=4, ensure_ascii=False)
    ...

# Надо сделать так, что б функция селениума вызывалась только тогда, когда при попытке запроса в категорию ответ != 200 приходил бы, ну или на каждую категорию получать кукиши..
def main():
    start = time.time()
    stores = get_all_stores_for_me(MY_COORDS)
    for store in stores[:1]:
        store_id, store_name, store_slug = get_info_about_store(store)
        all_category = parse_discount_category(get_discount_category(store))
        for category_name, category_url in all_category.items():
            if category_name == 'Овощи, фрукты, орехи':
                cookies = save_cookies_in_files_from_selenium(store, category_url, store_slug, store_id)
                scrap_one_category(store_id, store_name, category_url, category_name, cookies)
            time.sleep(2)
        time.sleep(3)
    print(f'Time processed: {time.time() - start} seconds')

def check_time(func):
    start = time.time()
    func()
    print(f'Time processed: {time.time() - start} seconds')

def main1():
    stores = get_all_stores_for_me(MY_COORDS)
    for i, store in enumerate(stores):
        print(f'{i})', store)
    choose_store = int(input('Выбери магазин из списка: '))
    print(f"Ты выбрал {choose_store}-й магазин")
    time.sleep(1)
    store_id, store_name, store_slug = get_info_about_store(stores[choose_store])
    all_category = parse_discount_category(get_discount_category(stores[int(choose_store)]))
    for i, category in enumerate(all_category.items()):
        print(f'{i})', category[0])
    choose_category = int(input('Выбери категорию из списка: '))
    print(f"Ты выбрал {choose_category}-ю категорию")
    time.sleep(1)
    cookies = save_cookies_in_files_from_selenium(stores[choose_store], tuple(all_category.items())[choose_category][1], store_slug, store_id)
    scrap_one_category(store_id, store_name, tuple(all_category.items())[choose_category][1], tuple(all_category.items())[choose_category][0], cookies)
    parse_category(store_name, tuple(all_category.items())[choose_category][0])
    

if __name__ == "__main__":
    # main1()
    check_time(main1)
    # parse_category('АШАН, Омск, бул. Архитекторов', 'Сыры')
    ...

# Надо реализовать это следующим путём:
# Буду получать магазины и уходить в условие и инпут:
    # Надо будет печатать через enumerate список магазинов в цикле
    # Спрашивать, какой магазин хочет выбрать пользователь
    # Запускать процесс parse_discount_category
    # Выводить все найденные скидочные категории (снова через цикл enumerate)
    # Просить выбрать категорию для парсинга
        # Запускать процесс получения cookies для данной категории через селениум и скрапить
            # После чего надо будет ещё распарсить полученные данные:
                # Привести в удобный вид JSON и отсортировать этот список словарей по значению(value) скидки на товар, которая просчитается при предыдущем этапе