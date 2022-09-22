import pprint
import sys
import os
import json
from pathlib import Path
import requests
import time
from selenium import webdriver
import pickle

# Добавляю в поиск путей корневую директорию всех файлов
sys.path.insert(1, os.getcwd())
from sbermarket_api.client import Client
from sbermarket_api.store import Store

PYTHON_PATH = Path(__file__)                    # Объект пути к исполняемому питоновскому файлу
DIR_MYWORK = PYTHON_PATH.parent                 # Путь, где расположен скрипт, который запускается
DATA_PATH = DIR_MYWORK / 'Data'                 # Путь, где хранятся данные, получаемые при работе скрипта. Задумывается, что в той же директории (рядом с файлом питона, который запускается) создаётся папка Data и там сохраняется всё под своими именами
MY_COORDS = {'lat': 54.92046, 'lon': 73.469722}
BASE_URL = 'https://sbermarket.ru/api/stores/STORE_ID/products'
URL_SELENIUM = 'https://sbermarket.ru'

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
        '''Запишу в объект класса список с доступными магазинами для доставки по указанным координатам. В дальнейшем буду иметь доступ к этому списку'''
        client = Client()
        stores = client.stores(coords['lat'], coords['lon'])    # -> list элементами этого списка являются объекты класса Store
        return stores


class ParsingStore:
    def __init__(self, stores: list[Store], headers: dict):
        self.stores = stores
        self.first_store = self.stores[0]
    
    def get_discount_category(self, store: Store) -> dict[str, str]:
        '''Получу всеее скидочные категории в переданном магазине в метод'''
        categories = store.categories()
        only_discount_category = categories['promoted_categories'][0]   # -> dict Вытаскиваю словарь только с обычными скидками (т.к. в первой вложенности есть ещё скидки до 60%)
        
        only_discount_category = {category['name']: category['canonical_url'].replace('https://sbermarket.ru/categories/', '') for category in only_discount_category['children']}  # Формирую удобный для работы словарь с наименованием категории и суффиксом url для базового url что б потом использовать для запроса
        
        # pprint.pprint(only_discount_category)   # Служебная инфа
        return only_discount_category
    
    def save_cookies_in_files_from_selenium(self, category: str, store: Store, slug_store: str):
        '''Запущу селениум, сделаю запрос на картегорию, нужную мне и сохраню куки в файл рядом с исполняемым файлом. В App V0.1 я это пробую сохранять в экземпляр класса, что б использовать без кучи открытия и записи и чтения файлов'''
        
        url = f'https://sbermarket.ru/{slug_store}/c/{category}?sid={store.id}&source=category'
        print(url)
        # return
        # options
        options = webdriver.ChromeOptions()
        # disable webdriver mode
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        with webdriver.Chrome(executable_path=r"E:\Python\Sber (Selenium)\chromedriver\chromedriver.exe", options=options) as driver:
            try:
                driver.get(url)
                time.sleep(10)
                # cookies
                # save on PC
                # pickle.dump(driver.get_cookies(), open('cookies', 'wb'))
                
                # work in process
                cookies = driver.get_cookies()
                self.cookies = {cookie.get('name'): cookie.get('value') for cookie in cookies}  # Сохраняю словарь cookies в объект класса, что б можно было потом использовать
            except Exception as ex:
                print('[!]', ex)
    
    def get_slug_store(self, store: Store):
        slug_store = Client().store(store.id).__dict__['retailer']['slug']
        return slug_store
    
    def collecting_items_in_category(self, category: str):
        pass
    
    def test(self):
        discount_categories = self.get_discount_category(self.first_store)

    def test_selenium(self):
        self.save_cookies_in_files_from_selenium(self.get_discount_category(self.first_store)['Овощи, фрукты, орехи'], self.first_store, self.get_slug_store(self.first_store))

def main():
    pars = ParsingStore(get_all_stores_for_me(MY_COORDS), headers)
    # pars.test()
    pars.test_selenium()

if __name__ == "__main__":
    main()