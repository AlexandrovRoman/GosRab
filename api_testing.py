from pprint import pprint

import requests

pprint(requests.post('http://127.0.0.1:5000/api/user', json={
    'name': 'Владимир',
    'surname': 'Владивирович',
    'fathername': 'Путин',
    'email': 'putin@email.com',
    'password': '123',
}).json())

pprint(requests.get('http://127.0.0.1:5000/api/user').json())
pprint(requests.get('http://127.0.0.1:5000/api/user/1').json())

