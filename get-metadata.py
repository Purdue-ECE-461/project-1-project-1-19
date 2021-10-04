from scoringscript import *
from github import Github
import os
import datetime as dt
import dateutil.relativedelta as du
import requests
from bs4 import BeautifulSoup
from bs4 import re


# import requests
# import json


# import numpy as np


def metadata_collect(url):
    # backup_url = url
    npm_flag = "https://www.npmjs.com"
    if npm_flag in url:
        headers = {'Accept-Encoding': 'identity'}
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        all_links = soup.find_all('a', href=re.compile(r'github\.com/'))
        url = all_links[0].get('href')

    url = url.replace("https://github.com/", "")

    token = os.getenv('GITHUB_TOKEN')
    # TOKEN= os.getenv('GITHUB_TOKEN')
    # url_license ="https://github.api.com/repos" + owner + repository + '/license'
    # print(url_license)
    # lic = requests.get(url_license).json()
    # print(lic)

    g = Github(token)
    repo = g.get_repo(url)
    # pulls = repo.get_contributors(anon="True")

    content_list = repo.get_contents("")
    p_list = []

    for elem in content_list:
        p_list.append(elem.path)

    git_name = 'LICENSE'
    print(p_list)
    if git_name in p_list:
        li = repo.get_license().decoded_content
        li = li.title().decode()
        ind = li.split()[0]
        if ind.lower() == "the":
            ind = li.split(' ')[1]
        # print(ind)
        if ind.lower() == "gnu" or ind.lower() == "affero" or ind.lower() == "bsd" or ind.lower() == "mit" \
                or ind.lower() == "apache":
            lic = 1
        else:
            lic = 0
    else:
        lic = 0

    git_name = 'README.md'
    if git_name in p_list:
        rm = 1
    else:
        rm = 0

    if repo.has_wiki:
        wiki = 1
    else:
        wiki = 0

    git_name = 'CONTRIBUTING.md'
    if (git_name or 'ISSUE_TEMPLATE') in p_list:
        contri = 1
    else:
        contri = 0

    today = dt.datetime.now()
    date_lm = today + du.relativedelta(months=-1)

    # trying to get issues from the last month
    issues_total1 = repo.get_issues(since=date_lm, state='all').totalCount
    issues_closed1 = repo.get_issues(since=date_lm, state='closed').totalCount
    if issues_total1:
        per_close_1 = (issues_closed1 / issues_total1) * 100
    else:
        per_close_1 = 0
    date_llm = date_lm + du.relativedelta(months=-1)
    issues_total2 = repo.get_issues(since=date_llm, state='all').totalCount - issues_total1
    issues_closed2 = repo.get_issues(since=date_llm, state='closed').totalCount - issues_closed1
    if issues_total2:
        per_close_2 = (issues_closed2 / issues_total2) * 100
    else:
        per_close_2 = 0

    date_lllm = date_llm + du.relativedelta(months=-1)
    issues_total3 = repo.get_issues(since=date_lllm, state='all').totalCount - issues_total1 - issues_total2
    issues_closed3 = repo.get_issues(since=date_lllm, state='closed').totalCount - issues_closed1 - issues_closed2
    if issues_total3:
        per_close_3 = (issues_closed3 / issues_total3) * 100
    else:
        per_close_3 = 0

    avg_per_close = (per_close_1 + per_close_2 + per_close_3) / 3
    # print(avg_per_close)

    cont = repo.get_contributors(anon='True').totalCount  # number of contributors for the repo
    issues_close_time = repo.get_issues(since=date_lm, state='closed')
    cr_time = []
    end_time = []
    # print((cr_time))
    iss_check = repo.get_issues(since=date_lm, state='closed').totalCount
    if iss_check > 0:
        for issues in issues_close_time:
            cr_time.append(issues.created_at.day)
            end_time.append(issues.closed_at.day)
        time_taken = [m - n for m, n in zip(end_time, cr_time)]
        avg_response_time = sum(time_taken) / len(time_taken)
        # print(avg_response_time)
    else:
        avg_response_time = 10000

    metadata_dict = {
        "readme": rm,  # Ramp-up score
        "contributing": contri,  # Ramp-up score
        "documentation": wiki,  # Ramp-up score
        "average %issues closed": avg_per_close,  # Correctness score
        "number_contributors": cont,  # Bus-factor score
        "average_time": avg_response_time,  # Responsive Maintainer Score
        "license": lic  # License score
    }
    return metadata_dict


def url_parser(filename):
    # urls = []
    with open(filename) as f:
        urls = f.read().splitlines()
    return urls


def api_url_generator(urls):
    github_api = "https://github.api.com"
    api_urls = []
    for url in urls:
        url = url.replace("https://github.com", "/repos")
        url = github_api + url
        api_urls.append(url)
    return api_urls


def main():
    filename = 'tests/test3.txt'
    urls = url_parser(filename)
    # api_urls = api_url_generator(urls)
    i = 0
    for url in urls:
        backup_url = url
        # print(url)
        metadata_dict = metadata_collect(url)
        # print(metadata_dict)
        scoring(backup_url, metadata_dict)
        i = i + 1


if __name__ == "__main__":
    main()
