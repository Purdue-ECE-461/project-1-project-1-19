import requests
from pprint import pprint


filename = "tests/test1.txt"
urls = []
data = []
with open(filename) as f:
    urls = f.read().splitlines()

for url in urls:
    ind = url.find("github")
    front = url[:ind]
    back = url[ind:]
    url = front + "api." + back
    print(url)



# number of contributors (in the last year)
# number of open/closed issues
