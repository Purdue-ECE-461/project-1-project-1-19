import requests
from pprint import pprint

url = f"https://api.github.com/repos/nullivex/nodist/commits"
data = requests.get(url).json()
pprint(data)
