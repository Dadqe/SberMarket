import json
from pprint import pprint

with open('list_products.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# pprint(data['products'])
# print(type(data['products']))
print(type(data))
print(len(data))