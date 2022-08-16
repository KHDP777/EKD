import json
import random
from time import sleep

from bs4 import BeautifulSoup
import requests
import csv


def get_date(url):
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"
    }
    req = requests.get(url, headers=headers)
    return req

url = "https://ekd.me/"

# src = get_date(url)

# with open(f"index.html", "w") as file:
#     file.write(src.text)

with open(f"index.html") as file:
    text_url = file.read()

soup = BeautifulSoup(text_url, "lxml")
all_tags = soup.find_all("h2", class_="entry-title")
date_index = {}
for item in all_tags:
    key = item.find("a").text
    rep = [", ", ": ", ". ", " ", "-", "\'", "«", "»"]
    for element in rep:
        if element in key:
            key = key.replace(element, "_")
    value = item.find("a").get("href")
    date_index[key] = value
# print(date_index)

with open("index.json", "w") as file:
    json.dump(date_index, file, indent=4, ensure_ascii=False)

with open("index.json") as file:
    date_index = json.load(file)

# print(date_index)

count = 0
project_list = []
for key, value in date_index.items():
    count += 1
    sleep(random.randrange(2, 4))
    all = int(len(date_index)) + 1
    print(f"Скачивается {count} файл из {all}")
    soup = get_date(value)
    with open(f"data/{count}_{key[:15]}.html", "w") as file:
        file.write(soup.text)

    with open(f"data/{count}_{key[:15]}.html") as file:
        src = file.read()
    current_soup = BeautifulSoup(src, "lxml")

    try:
        article_img = current_soup.find("figure", class_="wp-block-image size-full").find("img").get("src")
        print(article_img)
    except Exception:
        article_img = "No Logo"

    try:
        article_title = current_soup.find("h1", class_="entry-title").text
        print(article_title)
    except Exception:
        article_title = "No title"

    article_text = ''
    try:
        all_text = current_soup.find("div", class_="entry-content articlebody").find_all("p")
        for element in all_text:
            article_text += element.text
    except Exception:
        article_text = "No text"

    project_list.append(
        {
            "Название статьи" : article_title,
            "Ссылка на лого" : article_img,
            "Текст статьи" : article_text
        }
    )
    with open("project_data.json", "a", encoding="utf-8") as file:
        json.dump(project_list, file, indent=4, ensure_ascii=False)
