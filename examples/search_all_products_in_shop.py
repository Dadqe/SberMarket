# type: ignore[var-annotated]
"""Example of code."""
import sys
import os

# sys.path.insert(0, "/sbermarket-api") # Variant 1
# from sbermarket_api.client import Client # Variant 1

sys.path.insert(1, os.getcwd()) # Variant 2
from sbermarket_api.client import Client # Variant 2

if __name__ == "__main__":
    client = Client()                                       # Создаю Объект класса Client, что б использовать его методы
    # Получить все магазины доступные для данной точки.
    stores = client.stores(lat=60.003526, lon=30.253471)    # Использую метод Client.stores, передаю в него широту и долготу
    # Посмотреть, какие магазины программа нашла для данной точки. Возвращается 8 магазинов, прям как на сайте
    print(stores)
