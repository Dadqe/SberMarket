import json
import requests
from pprint import pprint
import time

# my_stores_list = [('METRO, Омск, Черлакский тракт', 152), ('АШАН, Омск, бул. Архитекторов', 235), ('ЛЕНТА, Омск, Сибирский', 699), ('МАГНИТ, Омск,Станционная 6-я', 3025), ('МАГНИТ СЕМЕЙНЫЙ, Омск, Станционная 6-я', 2167), ('МАГНИТ КОСМЕТИК, Омск,Сибирский пр-кт', 13573), ('FIX PRICE: БЫСТРАЯ ДОСТАВКА, Омск,Станционная 6-я', 6274), ('ПАРФЮМ ЛИДЕР: БЫСТРАЯ ДОСТАВКА, Омск,Станционная 6-я', 4082)]

with open(r'E:\SberMarket\mywork\Data\all_stores_for_me.json', 'r', encoding='utf-8') as f:
    my_stores_dict = json.load(f) # -> dict с магазинами для меня name: store_id
my_stores_list = list(my_stores_dict.items()) # -> list с магазинами внутри кортежи под каждый магазин (name, store_id)

with open(r'E:\SberMarket\mywork\Data\2_name_url_in_discount_category.json', 'r', encoding='utf-8') as f:
    discount_category = json.load(f) # -> dict с магазинами для меня name: store_id

# Пока работаю с овощами, фруктами, орехами. Там 3 страницы, для тестов хватит
# А так просто циклом for проходиться, брать значения, перекидывать в presub_url, потом трансформировать, вытаскивать нужную часть и прокидывать дальше
vegetable_url = discount_category.get('Овощи, фрукты, орехи') # https://sbermarket.ru/categories/priedlozhieniia/skidki/ovoshchi-frukti-orekhi

STORE_ID = my_stores_list[0][1]
BASE_URL = f'https://sbermarket.ru/api/stores/{STORE_ID}/products'
sub_url = vegetable_url.replace('https://sbermarket.ru/categories/', '') # Убираю типа BASE_URL или преффикс. Он мне не нужен. Для формирования запроса нужна только оставшаяся часть. Её я передам в словарь params для запроса. -> priedlozhieniia/skidki/ovoshchi-frukti-orekhi

cookies = {
    'iap.uid': 'ad0338003268462185ceab24d028e6a7',
    'city_info': '%7B%22slug%22%3A%22omsk%22%2C%22name%22%3A%22%D0%9E%D0%BC%D1%81%D0%BA%22%2C%22lat%22%3A54.9978%2C%22lon%22%3A73.4001%7D',
    'cookies_consented': 'yes',
    'identified_address': 'true',
    'user_is_adult': 'true',
}

headers = {
    'authority': 'sbermarket.ru',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru,en;q=0.9',
    'api-version': '3.0',
    'cache-control': 'no-cache',
    'client-token': '7ba97b6f4049436dab90c789f946ee2f',
    'referer': 'https://sbermarket.ru/metro/c/priedlozhieniia/skidki/alcohol-new?sid=152&source=category',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.3.822 Yowser/2.5 Safari/537.36',
}

# Эти параметры будут использоваться для первого запроса, что б получить данные и посчитать, сколько страниц товаров придётся проскрапить
params = {
    'tid': sub_url,
    'page': '1',
    'per_page': '20',
    'sort': 'popularity',
}
# response = requests.get(BASE_URL, params=params, cookies=cookies, headers=headers).json() # -> JSON Срази делаю ссылку на многовариативный запрос. Это будет первичный запрос для получения полной информации о товарах в данной категории из словарика по ключу 'meta' К нему надо напрямую обращаться, потому что он скрыт, возвращается сразу словарь по ключу 'products'
# А меня интересует: 'per_page', 'total_count' возможно и не надо, но на всякий случай, что б можно было потом проверять, не потерялось ли ничего, 'total_pages'

# with open(r'E:\SberMarket\mywork\Data\vegetables\meta.json', 'w', encoding='utf-8') as f:
#     json.dump(response['meta'], f, indent=4, ensure_ascii=False) # Записываю весь словарь meta в JSON

# with open(r'E:\SberMarket\mywork\Data\vegetables\meta.json', 'r', encoding='utf-8') as f:
#     meta_dict = json.load(f) # -> Беру из этого json данные
    
# print(meta_dict, type(meta_dict))
# total_pages = meta_dict['total_pages'] # Получаю количество всех страниц в данной категорией

# В цикле надо будет проходиться в range(1, total_pages + 1) Что б получалось 1, 2, 3
# Изменять страницу в словаре params, что б проскрапить все страницы с товарвами и отправлять запрос 

# for page in range(1, total_pages + 1):
#     params['page'] = str(page)
#     response = requests.get(BASE_URL, params=params, cookies=cookies, headers=headers)
#     time.sleep(1) # Лучше бы поспать, пока будем спать 1 секунду, но потом через рандоминт (1, 2) от 1 до 2 секунд мб сделать, что б не выглядеть, как бот. Пока 1 секунды достаточно, ответ положительный приходит
#     # params['page'] = '1' # Верну на всякий случай в изначальное значение. Что б следующая категория с 1 начинала запрос... Хотя она будет начинать вообще весь цикл с нуля...
    
    



# просто надо распарсить те данные, которые я получил при запросе в категорию, надо при первом запросе получить данные из "meta" там узнать, сколько всего товаров, разделить на 20, узнать сколько страниц надо будет скрапить, начать их скрапить и записывать в отдельную папочку. Сначала поработаю с json-файлами, потом можно будет сразу, скрапить, оттуда вытягивать нужную инфу и уже последний json-файл формить, который можно будет выдавать уже дальше куда-нибудь (например в табличку) или типа того
# разобраться с библиотекой path или что-то такое, что б там проверять на "создан ли уже файл и директория" Это для того момента, когда беру данные о скидочных категориях, потом по ним буду проходиться, скрапить и формаировать json-файл о каждой отдельной категории. Там надо будет аргумет "a" в контекстном менеджере писать, что б не засорять память, а по чуть-чуть добавлять. Про пагинацию речь











# with open(r'E:\SberMarket\mywork\Data\alco_first20.json', 'w', encoding='utf-8') as file:
#     json.dump(json.loads(response_text), file, indent=4, ensure_ascii=False) # Сначала я получаю type(dict) через команду json.loads, которая принимает аргуметом строку. А потом полученный словарь преобразую в json и сохраняю

# В списке ссылка 
# "https://sbermarket.ru/products/221437-brendi-torres-10-gran-reserva-38-0-5-l" её надо заменить как-то на
# 'https://sbermarket.ru/api/stores/152/products/brendi-torres-10-gran-reserva-38-0-5-l'
# Такая ссылка в запросе, когда кликаю на продукт
# Можно выдёргивать значение по ключу slug и посылать запрос на https://sbermarket.ru/api/stores/152/products/ + slug и там получу инфу о товаре, но она юзелесс