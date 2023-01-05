a = "https://sbermarket.ru/api/stores/699/products"
n = "v3"

i = a.find('/stores')

l = a[:i+1] + n + a[i:]
print(l)