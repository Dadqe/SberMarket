from typing import List

# from sbermarket_api.api import API
# from sbermarket_api.product import Product

import sys
import os

sys.path.insert(1, os.getcwd()) # Variant 2
from sbermarket_api.api import API
from sbermarket_api.product import Product


class Store:
    # При инициализации передаю сюда только ссылку на api and **store - список из словариков о каждом магазине (оттуда берётся каждый следующий словарь при ит-ии в [Store()..])
    def __init__(self, api: API, store_id: int, name: str, **kwargs):
        self.api = api
        self.id = None  # by get list it is uuid, by specific get store it is int
        self.store_id = store_id # Берёт из каждого словарика значение из ключа store_id
        self.name = name # и из ключа name и присваивает всё это локальным атрибутам
        self.__dict__.update(kwargs)
        # print(self.__dict__)

    def search_products(self, search: str, per_page: int = 24, page: int = 1) -> List[Product]:
        """Поиск по товарам per_page 24 это максимум"""
        query = {"q": search, "per_page": per_page, "page": page}
        response = self.api.request(f"stores/{self.store_id}/products", query=query)
        return [Product(self.api, **product) for product in response["products"]]

    def categories(self, depth: int = 2):  # type: ignore
        """Получить инфу по категориям, товаров там не будет"""
        query = {}
        if depth:
            query["depth"] = depth
        return self.api.request(f"stores/{self.store_id}/categories", query=query)

    def product(self, id: str) -> Product:
        """Получить инфу по одному товару"""
        url = f"stores/{self.store_id}/products/{id}"
        return Product(self.api, **self.api.request(url))

    def aggregating_categories(self):
        """на анонимной сесиии в ответ пустота: []"""
        url = f"stores/{self.store_id}/aggregating_categories"
        return Product(self.api, **self.api.request(url))

    def __repr__(self):
        return f"Store: {self.name}"




# Тест метода Client.stores() Проверял, что возвращает в итоге. Возвращает список магазинов в таком формате. Для удобатсва отображения в __repr__ перегрузил этот метод и всё, а так спокойно обращаться ко всем атрибутам можно
# api = API(base_url="https://sbermarket.ru/api/", client_token="7ba97b6f4049436dab90c789f946ee2f")

# kw = [{'id': '6090d3cd-fce4-48e0-afae-ab140a4b97a2', 'store_id': 152, 'name': 'METRO, Омск, Черлакский тракт', 'min_order_amount': 1000.0, 'min_order_amount_pickup': 500.0, 'min_first_order_amount': 1000.0, 'min_first_order_amount_pickup': 500.0, 'delivery_forecast_text': None, 'on_demand': False, 'express_delivery': False, 'minimum_order_amount': 1000.0, 'minimum_order_amount_pickup': 500.0, 'shipping_methods': [{'title': 'Курьером', 'type': 'by_courier'}, {'title': 'Курьером для компаний', 'type': 'by_courier_for_companies'}]}, 
#       {'id': 'cb4c6b56-78d1-445f-b4c5-00f340cb4d3b', 'store_id': 235, 'name': 'АШАН, Омск, бул. Архитекторов', 'min_order_amount': 2500.0, 'min_order_amount_pickup': 500.0, 'min_first_order_amount': 1000.0, 'min_first_order_amount_pickup': 500.0, 'delivery_forecast_text': None, 'on_demand': False, 'express_delivery': False, 'minimum_order_amount': 1000.0, 'minimum_order_amount_pickup': 500.0, 'shipping_methods': [{'title': 'Курьером', 'type': 'by_courier'}, {'title': 'Курьером для компаний', 'type': 'by_courier_for_companies'}]}, 
#       {'id': '90af0353-9d31-4707-a49b-e78ab0668db5', 'store_id': 699, 'name': 'ЛЕНТА, Омск, Сибирский', 'min_order_amount': 2500.0, 'min_order_amount_pickup': 500.0, 'min_first_order_amount': 1000.0, 'min_first_order_amount_pickup': 500.0, 'delivery_forecast_text': None, 'on_demand': False, 'express_delivery': False, 'minimum_order_amount': 1000.0, 'minimum_order_amount_pickup': 500.0, 'shipping_methods': [{'title': 'Курьером', 'type': 'by_courier'}, {'title': 'Курьером для компаний', 'type': 'by_courier_for_companies'}]}, 
#       {'id': 'ee640a11-3b99-48b4-8574-3d180b0afde2', 'store_id': 3025, 'name': 'МАГНИТ, Омск,Станционная 6-я', 'min_order_amount': 500.0, 'min_order_amount_pickup': 0.0, 'min_first_order_amount': 300.0, 'min_first_order_amount_pickup': 0.0, 'delivery_forecast_text': '95–125 мин', 'on_demand': True, 'express_delivery': False, 'minimum_order_amount': 300.0, 'minimum_order_amount_pickup': 0.0, 'shipping_methods': [{'title': 'Курьером', 'type': 'by_courier'}, {'title': 'Курьером для компаний', 'type': 'by_courier_for_companies'}]}, 
#       {'id': 'e7fa43e9-e47a-4708-888c-888ddf90eb6a', 'store_id': 2167, 'name': 'МАГНИТ СЕМЕЙНЫЙ, Омск, Станционная 6-я', 'min_order_amount': 1000.0, 'min_order_amount_pickup': 1000.0, 'min_first_order_amount': 1000.0, 'min_first_order_amount_pickup': 1000.0, 'delivery_forecast_text': None, 'on_demand': False, 'express_delivery': False, 'minimum_order_amount': 1000.0, 'minimum_order_amount_pickup': 1000.0, 'shipping_methods': [{'title': 'Курьером', 'type': 'by_courier'}, {'title': 'Курьером для компаний', 'type': 'by_courier_for_companies'}]}, 
#       {'id': '269d3a3e-cc1a-481b-8755-68e08729e63a', 'store_id': 13573, 'name': 'МАГНИТ КОСМЕТИК, Омск,Сибирский пр-кт', 'min_order_amount': 500.0, 'min_order_amount_pickup': 0.0, 'min_first_order_amount': 300.0, 'min_first_order_amount_pickup': 0.0, 'delivery_forecast_text': '80–110 мин', 'on_demand': True, 'express_delivery': False, 'minimum_order_amount': 300.0, 'minimum_order_amount_pickup': 0.0, 'shipping_methods': [{'title': 'Курьером', 'type': 'by_courier'}, {'title': 'Курьером для компаний', 'type': 'by_courier_for_companies'}]}, 
#       {'id': '190052d6-35ed-49f9-ad3b-2f7426ef9e51', 'store_id': 6274, 'name': 'FIX PRICE: БЫСТРАЯ ДОСТАВКА, Омск,Станционная 6-я', 'min_order_amount': 700.0, 'min_order_amount_pickup': 0.0, 'min_first_order_amount': 300.0, 'min_first_order_amount_pickup': 0.0, 'delivery_forecast_text': None, 'on_demand': False, 'express_delivery': False, 'minimum_order_amount': 300.0, 'minimum_order_amount_pickup': 0.0, 'shipping_methods': [{'title': 'Курьером', 'type': 'by_courier'}, {'title': 'Курьером для компаний', 'type': 'by_courier_for_companies'}]}, 
#       {'id': 'f7f01033-ff2b-4bd5-a427-01af1b51f119', 'store_id': 4082, 'name': 'ПАРФЮМ ЛИДЕР: БЫСТРАЯ ДОСТАВКА, Омск,Станционная 6-я', 'min_order_amount': 500.0, 'min_order_amount_pickup': 0.0, 'min_first_order_amount': 300.0, 'min_first_order_amount_pickup': 0.0, 'delivery_forecast_text': '90–120 мин', 'on_demand': True, 'express_delivery': False, 'minimum_order_amount': 300.0, 'minimum_order_amount_pickup': 0.0, 'shipping_methods': [{'title': 'Курьером', 'type': 'by_courier'}, {'title': 'Курьером для компаний', 'type': 'by_courier_for_companies'}]}]

# def test(api, kw):
#     return [Store(api, **store) for store in kw]

# out = test(api, kw)
# print(out)

def main():
    api = API(base_url="https://sbermarket.ru/api/", client_token="7ba97b6f4049436dab90c789f946ee2f")
    

if __name__ == '__main__':
    main()