import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYm90IiwiaWQiOiJycGkifQ.8Wofl6FxJZosF-wpceQA4UG-6LYjGV0DddYYpEedr1g"

headers = {'User-Agent': '*', "Authorization": f"Bearer {token}"}


url = "http://127.0.0.1:5000/api/door/ping"

json_data = requests.get(url, headers=headers).json()

print(json_data)