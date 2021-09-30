import requests
from pprint import pprint

username = "ric-rhee"
url = f"https://api.github.com/users/{username}"
#url = f"https://api.github.com/nullivex/nodist"
user_data = requests.get(url).json()
pprint(user_data)