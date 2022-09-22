from typing import Any, Dict, List, Union

from urllib.parse import urljoin

import requests
from requests import JSONDecodeError


class ApiError(Exception):
    pass


class API:
    def __init__(self, base_url: str, client_token: str):
        self.__client_token = client_token
        self.base_url = base_url

    def request(self, url, auth=True, query: Dict[str, Any] = None):  # type: ignore
        
        full_url = urljoin(self.base_url, url) # Объединяю базовый url = "https://sbermarket.ru/api/" и относительную часть пути = "stores" https://sbermarket.ru/api/stores/152/categories
        print(f'Full_url: {full_url}') # Для себя для общего понимания пишу
        headers = {"accept": "application/json, text/plain, */*", "api-version": "3.0"} # headers для request.get
        if auth:
            headers["client-token"] = self.__client_token # Добавляю в headers ключ: значение для токена
        resp = requests.get(full_url, headers=headers, params=query) # query = {"lat": lat, "lon": lon, "shipping_method": shipping_method="delivery"}
        print('URL for resp', resp.url) # Для себя для общего понимания пишу
        try:
            result = resp.json() # получаю информацию о магазинах в json
            if "error" in result:
                raise ApiError(result["error"])
            return result # Возвращаю список словарей, где каждый словарь выступает информацией об одном каждом магазине
        except JSONDecodeError as e:
            raise ApiError("Unexpected not json response. Can't parse.")
        except Exception as e:
            raise e


# Для того, что б найти, какой, что и как формируется следующий запрос, что б получить инфу о ближайших магаз
# Триггернул я только тем, что по новой выбрал адрес на главной странице:
# Request URL: https://sbermarket.ru/api/stores?lat=54.92046&lon=73.469722&include=closest_shipping_options%2Clabels%2Cretailer%2Clabel_store_ids&shipping_method=delivery

query={"lat": 54.92046, "lon": 73.469722, "shipping_method": "delivery"}
test = API("https://sbermarket.ru/api/", "7ba97b6f4049436dab90c789f946ee2f")
# response = test.request("stores", True, query=query) # Получаю списочек со словарями магазинов, главной инфы о них, которые для меня доступны, исходя из адреса




# ToDo research
# "https://sbermarket.ru/api/auth_providers/sberbank/auth_params"
# "https://sbermarket.ru/api/next/page/browser_head"
# "https://sbermarket.ru/api/phone_confirmations"
# "https://sbermarket.ru/api/stores/1/next_deliveries?cargo=false"
# "https://sbermarket.ru/_next/static/chunks/pages/_app-b824ce51c817753c.js"
