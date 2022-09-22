import pprint
import sys
import os
import json
from pathlib import Path
import requests
import time

# Добавляю в поиск путей корневую директорию всех файлов
sys.path.insert(1, os.getcwd())
from sbermarket_api.client import Client
from sbermarket_api.store import Store

PYTHON_PATH = Path(__file__)                    # Объект пути к исполняемому питоновскому файлу
DIR_MYWORK = PYTHON_PATH.parent                 # Путь, где расположен скрипт, который запускается
DATA_PATH = DIR_MYWORK / 'Data'                 # Путь, где хранятся данные, получаемые при работе скрипта. Задумывается, что в той же директории (рядом с файлом питона, который запускается) создаётся папка Data и там сохраняется всё под своими именами
MY_COORDS = {'lat': 54.92046, 'lon': 73.469722}
BASE_URL = 'https://sbermarket.ru/api/stores/STORE_ID/products'

cookies = {
    'external_analytics_anonymous_id': '4d0ee956-f8c4-4ded-be03-91367b37f4c7',
    '_pk_id.6.3ec0': 'ca49ced8ccb50c1a.1660973634.',
    '_sa': 'SA1.d20313f0-ad34-4765-a1a1-c4935f8f230d.1660973634',
    'iap.uid': 'ad0338003268462185ceab24d028e6a7',
    'city_info': '%7B%22slug%22%3A%22omsk%22%2C%22name%22%3A%22%D0%9E%D0%BC%D1%81%D0%BA%22%2C%22lat%22%3A54.9978%2C%22lon%22%3A73.4001%7D',
    'sessionId': '16631757982601046093',
    'ngenix_jscv_cd881f1695eb': 'cookie_signature=KZg8eUGWZ2U2EAQ1uC5N65reOyc%3D&cookie_expires=1663176997',
    '_pk_ses.6.3ec0': '1',
    'ssrMedia': '{%22windowWidth%22:880%2C%22primaryInput%22:%22mouse%22}',
    'identified_address': 'true',
    '_808db7ba1248': '%5B%7B%22source%22%3A%22sbermarket.ru%22%2C%22medium%22%3A%22referral%22%2C%22cookie_changed_at%22%3A1663176954%7D%2C%7B%22source%22%3A%22cityads%22%2C%22medium%22%3A%22cpa%22%2C%22campaign%22%3A%225dRy%22%2C%22term%22%3A%229nkZ1WWFi0ZEyBz%22%2C%22cookie_changed_at%22%3A1660973636%7D%2C%7B%22source%22%3A%22%28direct%29%22%2C%22medium%22%3A%22%28none%29%22%2C%22cookie_changed_at%22%3A1663176956%7D%2C%7B%22source%22%3A%22cityads%22%2C%22medium%22%3A%22cpa%22%2C%22campaign%22%3A%225dRy%22%2C%22term%22%3A%229nkZ1WWHogZe7xB%22%2C%22cookie_changed_at%22%3A1660981461%7D%2C%7B%22source%22%3A%22cityads%22%2C%22medium%22%3A%22cpa%22%2C%22campaign%22%3A%225dRy%22%2C%22term%22%3A%229nkZ1WWJSnZiuUx%22%2C%22cookie_changed_at%22%3A1660990739%7D%2C%7B%22source%22%3A%22cityads%22%2C%22medium%22%3A%22cpa%22%2C%22campaign%22%3A%225dRy%22%2C%22term%22%3A%229nkZ1WXe85Zrpd3%22%2C%22cookie_changed_at%22%3A1661099545%7D%2C%7B%22source%22%3A%22cityads%22%2C%22medium%22%3A%22cpa%22%2C%22campaign%22%3A%225dRy%22%2C%22term%22%3A%229nkZ1WXWiFZ5oh0%22%2C%22cookie_changed_at%22%3A1661263915%7D%2C%7B%22source%22%3A%22cityads%22%2C%22medium%22%3A%22cpa%22%2C%22campaign%22%3A%225dRy%22%2C%22term%22%3A%229nkZ1WY9okZ9MC0%22%2C%22cookie_changed_at%22%3A1661308915%7D%2C%7B%22source%22%3A%22cityads%22%2C%22medium%22%3A%22cpa%22%2C%22campaign%22%3A%225dRy%22%2C%22cookie_changed_at%22%3A1661355750%7D%2C%7B%22source%22%3A%22cityads%22%2C%22medium%22%3A%22cpa%22%2C%22campaign%22%3A%225dRy%22%2C%22content%22%3A%223854r%22%2C%22term%22%3A%229nkZ1X1ghJZ9GVw%22%2C%22cookie_changed_at%22%3A1661788519%7D%2C%7B%22source%22%3A%22cityads%22%2C%22medium%22%3A%22cpa%22%2C%22campaign%22%3A%225dRy%22%2C%22content%22%3A%223854r%22%2C%22term%22%3A%229nkZ1X7jktZe8iC%22%2C%22cookie_changed_at%22%3A1663161735%7D%2C%7B%22source%22%3A%22cityads%22%2C%22medium%22%3A%22cpa%22%2C%22campaign%22%3A%225dRy%22%2C%22content%22%3A%223854r%22%2C%22term%22%3A%229nkZ1X7lqRZrqUK%22%2C%22cookie_changed_at%22%3A1663169567%7D%5D',
    '_Instamart_session': 'N0l3ZWIxeVhOYW9SazBlTHJGcHZpVzBtaFI2UDF5aHpWdmF0eTJzV3JNVEZUTHJhak84ZXlMS3FjQW5NbVNXcDVaR1FrQWU2SWJKY0pKK2RSaXc1ejA3MzU4NVV4eVQ1bjhiUVE1eGJpZFRubkFOa1lHWDRGQWxhZ0s1N25lRTJUVXc1bGErSHNMRUlWdnhjelQ4NDVLcUEyUS9FR0xTNndHUTkraGZOVmxXb0xmUStseUlNVENLUHA0dytPNHB3RjZ3SGlITG43NkUwMmo1WENGZmg4UT09LS1lcmdYa1FkS0Y1Zm5MaG4rTVpmTTR3PT0%3D--ec7bf0543203697f47b844db0f98b03f165f51d1',
}

headers = {
    'authority': 'sbermarket.ru',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru,en;q=0.9',
    'api-version': '3.0',
    'cache-control': 'no-cache',
    'client-token': '7ba97b6f4049436dab90c789f946ee2f',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'external_analytics_anonymous_id=4d0ee956-f8c4-4ded-be03-91367b37f4c7; _pk_id.6.3ec0=ca49ced8ccb50c1a.1660973634.; _sa=SA1.d20313f0-ad34-4765-a1a1-c4935f8f230d.1660973634; iap.uid=ad0338003268462185ceab24d028e6a7; city_info=%7B%22slug%22%3A%22omsk%22%2C%22name%22%3A%22%D0%9E%D0%BC%D1%81%D0%BA%22%2C%22lat%22%3A54.9978%2C%22lon%22%3A73.4001%7D; sessionId=16631757982601046093; ngenix_jscv_cd881f1695eb=cookie_signature=KZg8eUGWZ2U2EAQ1uC5N65reOyc%3D&cookie_expires=1663176997; _pk_ses.6.3ec0=1; ssrMedia={%22windowWidth%22:880%2C%22primaryInput%22:%22mouse%22}; identified_address=true; _808db7ba1248=%5B%7B%22source%22%3A%22sbermarket.ru%22%2C%22medium%22%3A%22referral%22%2C%22cookie_changed_at%22%3A1663176954%7D%2C%7B%22source%22%3A%22cityads%22%2C%22medium%22%3A%22cpa%22%2C%22campaign%22%3A%225dRy%22%2C%22term%22%3A%229nkZ1WWFi0ZEyBz%22%2C%22cookie_changed_at%22%3A1660973636%7D%2C%7B%22source%22%3A%22%28direct%29%22%2C%22medium%22%3A%22%28none%29%22%2C%22cookie_changed_at%22%3A1663176956%7D%2C%7B%22source%22%3A%22cityads%22%2C%22medium%22%3A%22cpa%22%2C%22campaign%22%3A%225dRy%22%2C%22term%22%3A%229nkZ1WWHogZe7xB%22%2C%22cookie_changed_at%22%3A1660981461%7D%2C%7B%22source%22%3A%22cityads%22%2C%22medium%22%3A%22cpa%22%2C%22campaign%22%3A%225dRy%22%2C%22term%22%3A%229nkZ1WWJSnZiuUx%22%2C%22cookie_changed_at%22%3A1660990739%7D%2C%7B%22source%22%3A%22cityads%22%2C%22medium%22%3A%22cpa%22%2C%22campaign%22%3A%225dRy%22%2C%22term%22%3A%229nkZ1WXe85Zrpd3%22%2C%22cookie_changed_at%22%3A1661099545%7D%2C%7B%22source%22%3A%22cityads%22%2C%22medium%22%3A%22cpa%22%2C%22campaign%22%3A%225dRy%22%2C%22term%22%3A%229nkZ1WXWiFZ5oh0%22%2C%22cookie_changed_at%22%3A1661263915%7D%2C%7B%22source%22%3A%22cityads%22%2C%22medium%22%3A%22cpa%22%2C%22campaign%22%3A%225dRy%22%2C%22term%22%3A%229nkZ1WY9okZ9MC0%22%2C%22cookie_changed_at%22%3A1661308915%7D%2C%7B%22source%22%3A%22cityads%22%2C%22medium%22%3A%22cpa%22%2C%22campaign%22%3A%225dRy%22%2C%22cookie_changed_at%22%3A1661355750%7D%2C%7B%22source%22%3A%22cityads%22%2C%22medium%22%3A%22cpa%22%2C%22campaign%22%3A%225dRy%22%2C%22content%22%3A%223854r%22%2C%22term%22%3A%229nkZ1X1ghJZ9GVw%22%2C%22cookie_changed_at%22%3A1661788519%7D%2C%7B%22source%22%3A%22cityads%22%2C%22medium%22%3A%22cpa%22%2C%22campaign%22%3A%225dRy%22%2C%22content%22%3A%223854r%22%2C%22term%22%3A%229nkZ1X7jktZe8iC%22%2C%22cookie_changed_at%22%3A1663161735%7D%2C%7B%22source%22%3A%22cityads%22%2C%22medium%22%3A%22cpa%22%2C%22campaign%22%3A%225dRy%22%2C%22content%22%3A%223854r%22%2C%22term%22%3A%229nkZ1X7lqRZrqUK%22%2C%22cookie_changed_at%22%3A1663169567%7D%5D; _Instamart_session=N0l3ZWIxeVhOYW9SazBlTHJGcHZpVzBtaFI2UDF5aHpWdmF0eTJzV3JNVEZUTHJhak84ZXlMS3FjQW5NbVNXcDVaR1FrQWU2SWJKY0pKK2RSaXc1ejA3MzU4NVV4eVQ1bjhiUVE1eGJpZFRubkFOa1lHWDRGQWxhZ0s1N25lRTJUVXc1bGErSHNMRUlWdnhjelQ4NDVLcUEyUS9FR0xTNndHUTkraGZOVmxXb0xmUStseUlNVENLUHA0dytPNHB3RjZ3SGlITG43NkUwMmo1WENGZmg4UT09LS1lcmdYa1FkS0Y1Zm5MaG4rTVpmTTR3PT0%3D--ec7bf0543203697f47b844db0f98b03f165f51d1',
    'is-storefront-ssr': 'false',
    'pragma': 'no-cache',
    'referer': 'https://sbermarket.ru/metro/c/priedlozhieniia/skidki/ovoshchi-frukti-orekhi',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Yandex";v="22"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.5.1027 Yowser/2.5 Safari/537.36',
}


def get_all_stores_for_me(coords) -> Store:# -> list[Store]:
    '''Верну в программу список с доступными магазинами для доставки по указанным координатам. Пока работает с одним магазином!!! Потом надо будет возвращать все и перебором в цикле работать!!!'''
    client = Client()
    stores = client.stores(coords['lat'], coords['lon'])    # -> list элементами этого списка являются объекты класса Store
    first_store = stores[0]                                 # Выбираю первый магазин для дальнейших тестов объект Store
    return first_store
    
def get_discount_category(store: Store) -> tuple[dict, str]:    # Вернётся кортеж с категориями и названием магазина, что б потом создать папку нужную
    '''Получу всеее скидочные категории'''
    categories = store.categories()                   # Получаю все категории, которые есть в переданном магазине
    only_discount_category = categories['promoted_categories'][0] # -> dict Вытаскиваю словарь только с обычными скидками (т.к. в первой вложенности есть ещё скидки до 60%)
    return only_discount_category, store.name

def save_only_discount_category(name_store: str, categories: dict, data_path: Path = DATA_PATH):
    '''Сохраню полученную информацию о скидочных категориях в формате JSON в папке Data в папку с названием магазина'''
    # создаю объект пути к сохранению данных, получаемых при запросах. Если папок нет, то создаю их
    MAGAZIN_PATH = data_path / name_store
    if not MAGAZIN_PATH.exists():
        data_path.mkdir(exist_ok=True)
        MAGAZIN_PATH.mkdir()
    
    # Записываю все скидочные категории категории в магазине 
    with open(f'{MAGAZIN_PATH}/only_discount_category.json', 'w', encoding='utf-8') as file:
        json.dump(categories, file, indent=4, ensure_ascii=False)

def parse_discount_category(name_store: str, data_path: Path = DATA_PATH):
    '''Распарсю большой json с категориями, приведу в более нужный вид, удобный для понимания и дальнейшей работы.'''
    path = data_path / name_store       # Путь к папке, где должен лежать необходимый файл JSON со всеми скидочными категориями по магазину
    with open(path / 'only_discount_category.json', 'r', encoding='utf-8') as file:
        data = json.load(file)          # Получаю dict
    
    name_url_in_discount_category = {category['name']: category['canonical_url'].replace('https://sbermarket.ru/categories/', '') for category in data['children']}  # Создаю словарь с название категории: url по которому смогу делать запрос и парсить дальше товары из категории. Сразу отрезал от ссылки ненужный префикс, базовый url, т.к. для запроса нужно будет передать в словарь params преобразованную ссылку
    
    with open(path / 'name_url_in_discount_category.json', 'w', encoding='utf-8') as file:
        json.dump(name_url_in_discount_category, file, indent=4, ensure_ascii=False)

def get_one_category(name_store: str, data_path: Path = DATA_PATH):
    '''Получаю одну категорию, что б дальше её передать. После всех тестов и отладок либо избавиться от этой функции либо гонять её в цикле вместе с чем-то, что б программа проходилась по одной категории, собирала инфу, переходила к другой. Если надо. Но вроде в моменте надо получать только по одной категории 👆.
    Надо будет предлагать категорию, и что б по индексу в этой функции выбиралась нужная категория. Индекс, это если в консоли будет программка работать, иначе с ткинтером снова баловаться, выставлять кнопочки, на каждую кнопочку придётся пермачом вешать ссылку и т.п.🥲'''
    path = data_path / name_store       # Путь к папке, где должен лежать необходимый файл JSON со всеми скидочными категориями по магазину
    with open(path / 'name_url_in_discount_category.json', 'r', encoding='utf-8') as file:
        data = json.load(file)          # Получаю dict
    return data['Овощи, фрукты, орехи'] # Сейчас верну такую категорию, а потом всё надо будет переделывать под циклы, это уже будет вторая функция, которую в цикле запускать придётся

def scrap_one_category(category: str, store_id: str, name_store: str, base_url: str = BASE_URL, data_path: Path = DATA_PATH):
    BASE_URL = base_url.replace('STORE_ID', store_id)
    page = 1
    
    MAGAZIN_PATH = data_path / name_store
    
    params = {
    'tid': category,
    'page': str(page),
    'per_page': '20',
    'sort': 'popularity',
    }
    
    my_items_list = []
    
    response = requests.get(BASE_URL, params=params, cookies=cookies, headers=headers, timeout=10)
    response = response.json()
    # response = requests.get(BASE_URL, params=params, cookies=cookies, headers=headers, timeout=10).json()   # -> JSON
    total_pages = response['meta']['total_pages']
    # total_count = response['meta']['total_count']
    
    
    
    items_list = response['products']
    # name_category = response['root_categories']['options']['name']
    
    for item in items_list:
        dict_of_item = {}
        name = item['name']
        price = item['price']
        discount_percentage = int((1 - (price / item['original_price'])) * 100)
        canonical_url = item['canonical_url']
        dict_of_item[name] = (price, discount_percentage, canonical_url)
        my_items_list.append(dict_of_item)
    
    with open(MAGAZIN_PATH / 'Овощи, фрукты, орехи.json', 'a', encoding='utf-8') as file:
        json.dump(my_items_list, file, indent=4, ensure_ascii=False)


    
    
    

def main():
    # first_store = get_all_stores_for_me(MY_COORDS)
    # only_discount_category, name_store = get_discount_category(first_store)
    # save_only_discount_category(name_store, only_discount_category)
    # parse_discount_category('METRO, Омск, Черлакский тракт')
    one_category = get_one_category('METRO, Омск, Черлакский тракт')
    scrap_one_category(one_category, '152', 'METRO, Омск, Черлакский тракт')

if __name__ == "__main__":
    main()


# Request URL: https://sbermarket.ru/api/stores/152/products?tid=priedlozhieniia%2Fskidki%2Fovoshchi-frukti-orekhi&page=2&per_page=20&sort=popularity


# with open(r"E:\SberMarket\examples\Data\alco\alco_first20.json", 'r', encoding='utf-8') as f:
#     data = json.load(f) # Получаю dict

# necessary_data = {}
# for product in data['products'][:2]:
#     name = product['name']
#     price = product['price']
#     discount_percent = int((1 - (price / product["original_price"])) * 100)
#     necessary_data[name] = (price, discount_percent)

# print(necessary_data)

# set-cookie: _Instamart_session=RjFOYi8xY1djakQ0NlcwTksxVU9ZMWIyenphb0Vxa1ZpTlltNVdLVXJuRkZ4KzJVNlRhblZQYitZbHlCNVREYjlrRmJuNmRPa2RpUUc2aHBYMjdJM2s5STYrUDJtOEVtbElpVnhweUNjZGNyd0xSd2czRW9SUDBKRUQ0TW1jaGMybkZrN3BTRlFSemc2NjFvOHlmREJWazFKS1FxN2Z6cE1uUGhHZXJyeE9vbVY1MGFya1NpMWhSVXo4SHpvQjB6LS14dzRnMCtxMjRKQXNvaGs1T3R6S25RPT0%3D--d0580bd9cc7e614a1a63c3b9fe31f97a53340f28; path=/; HttpOnly; SameSite=Lax
