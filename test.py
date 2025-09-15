import requests
import dotenv
import os

dotenv.load_dotenv()
token = os.getenv('BOT_TOKEN')

headers = {'User-Agent': '*', "Authorization": f"Bearer {token}"}

url = "https://dash.cssc.asn.au/api/door/ping"

json_data = requests.get(url, headers=headers).json()

print(json_data)