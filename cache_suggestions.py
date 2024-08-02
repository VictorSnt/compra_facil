import requests

respose = requests.api.get(
    'http://192.168.0.250:5912/report/cache_suggestions?repositions_days=30'
)
if (respose.status_code == 200):
    print('sucesso')
else:
    print('deu ruim')