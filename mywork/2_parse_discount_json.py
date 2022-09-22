import json

# Сначала открою файл на чтение
with open(r'E:\SberMarket\mywork\Data\only_discount_category.json', 'r', encoding='utf-8') as f:
    data = json.load(f) # Получаю dict

name_url_in_discount_category = {} # Наполню этот словарь, после чего json.dump сделать надо будет и сформировать отдельный json или просто текстовичок, не ясно до конца.
# Прихожу к скрапингу этого словаря, что б получить необходимые элементы

for category in data["children"]:
    '''Получаю имя категории
    Ссылку на категорию...НО!
    Эту ссылку придётся перерабатывать, потому что она должна идти с post-атрибутами, что б бралась из нужного магазина, позже сформирую эту ссылку и проверю. Т.к. если брать и переходить по этой ссылке, то получается, браузер откроет эту категорию в том магазине в котором ты сидел последний раз через браузер
    '''
    name = category["name"]
    canonical_url = category["canonical_url"]
    name_url_in_discount_category[name] = canonical_url

with open(r'E:\SberMarket\examples\Data\name_url_in_discount_category.json', 'w', encoding='utf-8') as file:
    json.dump(name_url_in_discount_category, file, indent=4, ensure_ascii=False)

# надо эти категории преобразовать, взять и просплитовать, и куда-то что-то засунуть
# должно получиться что-то типа: https://sbermarket.ru/api/stores/152/products?tid=priedlozhieniia%2Fskidki%2Falcohol-new&page=2&per_page=20&sort=popularity
# создать функцию сразу под это, что б можно было передавать, сколько мне надо страниц и т.к., когда буду вычислять исходя из того, сколько всего товара в этой категории и циклом пробегаться и получать