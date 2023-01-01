a = [
    {
        "name": "Сыр рассольный Galbani Моцарелла 45% 125 г",
        "price": 161.02,
        "discount_percent": 4
    },
    {
        "name": "Сыр рассольный Сиртаки Original комбинированный для греческого салата 55% 200 г",
        "price": 104.41,
        "discount_percent": 24
    },
    {
        "name": "Сыр полутвердый Arla Natura Сливочный 45% 200 г",
        "price": 202.82,
        "discount_percent": 4
    },
    {
        "name": "Плавленый сыр Hochland Фетакса 45% БЗМЖ 400 г",
        "price": 219.0,
        "discount_percent": 33
    },
    {
        "name": "Сыр твердый Dolce Granto Пармезан тертый 40% БЗМЖ 150 г",
        "price": 227.52,
        "discount_percent": 4
    },
    {
        "name": "Сыр полутвердый Сыробогатов Сливочный 50%",
        "price": 174.0,
        "discount_percent": 12
    }
]

b = sorted(a, key=lambda product: product['discount_percent'])

print(a)
print(b)