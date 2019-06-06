import requests
from my_fake_useragent import UserAgent

URL = 'https://pastr.io/login'
client = requests.Session()

ua = UserAgent()
print(ua.random())
header = {'User-Agent': str(ua.random())}

login_payload = {
    "email": "demonmanoj@gmail.com",
    "password": "Dem0n123@",
    "remember": False,
}

r = client.post(URL, data=login_payload, headers=header)
print(r)
