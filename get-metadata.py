import requests
from github import Github
import os
from pprint import pprint
import pandas as pd
import numpy as np

TOKEN= os.getenv('GITHUB_TOKEN')
# TOKEN= os.getenv('GITHUB_TOKEN')
g = Github(TOKEN)
repo = g.get_repo("Saumyanavani/Test")
pulls = repo.get_contributors(anon="True")
contents = repo.get_contents("")
file_n = []
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
    else:
        file = file_content
        file_n.append(str(file).replace('ContentFile(path="','').replace('")',''))

git_name = 'LICENSE'
if git_name in file_n:
    li = repo.get_license().decoded_content
    li = li.title().decode()
    ind = li.split()[0]
    if ind.lower() == "gnu" or ind.lower() == "affero" or ind.lower() == "bsd" or ind.lower() == "mit":
        lic = 1
    else:
        lic = 0
else:
    lic = 0

git_name = 'README.md'
if git_name in file_n:
    rm = 1
else:
    rm = 0

if repo.has_wiki:
    wiki = 1
else:
    wiki = 0

git_name = 'CONTRIBUTING.md'
if git_name in file_n:
    contri = 1
else:
    contri =0

print("Readme: ", rm)
print("WIKI: ", wiki)
print("CONTRIBUTING: ", contri)



