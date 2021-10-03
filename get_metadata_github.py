import json
import requests
from pprint import pprint


REPOS = '/repos'
GITHUB_API = 'https://api.github.com'


def main():
    filename = 'tests/test1.txt'
    data = {}
    dataTitles = ['commits', 'issues', 'branches', 'license']

    urls = url_parser(filename)
    api_urls = api_url_generator(urls)
    get_license(api_urls[0])


def url_parser(filename):
    urls = []
    with open(filename) as f:
        urls = f.read().splitlines()

    return urls


def api_url_generator(urls):
    api_urls = []
    for url in urls:
        ind = url.find('/', 15)
        back = url[ind:]
        api_url = GITHUB_API + back
        api_urls.append(api_url)

    return api_urls


def parse_url_owner_repo(url):
    slash_owner = url.find('/', 15)
    slash_repo = url.rfind('/')
    owner = url[slash_owner:slash_repo]
    repo = url[slash_repo:]
    print(owner)
    print(repo)

    return owner, repo


def get_commits(api_url):
    owner, repo = parse_url_owner_repo(api_url)
    url_commits = GITHUB_API + REPOS + owner + repo + '/commits'
    commits = requests.get(url_commits).json()


def get_license(api_url):
    owner, repo = parse_url_owner_repo(api_url)
    url_license = GITHUB_API + REPOS + owner + repo + '/license'
    lic = requests.get(url_license).json()


# number of contributors (in the last year)
# number of open/closed issues

main()
