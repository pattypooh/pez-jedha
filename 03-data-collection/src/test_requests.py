import requests

def test_get():
    payload = {'username':'pez', 'password': 'secret'}
    r = requests.post('https://httpbin.org/post', data=payload)


    r_dict = r.json()

    print(r_dict)

def test_auth():
    r= requests.get('https://httpbin.org/basic-auth/pez/secret', auth=('pez', 'secret'), timeout=3)
    print(r)
    print(r.text)

def test_timeout():
    r= requests.get('https://httpbin.org/delay/4', timeout=3)
    print(r)
    print(r.text)


test_timeout()