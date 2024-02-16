import os

import requests
import shutil

SITE_URL = "https://vc.ru"

PAGES_DIR = "data"
PAGES_NUMBER = 100
DOWNLOADING_FILES_OUTPUT = "выкачка"


def crawl_and_save_articles(start_id: int, num_articles: int):
    print("Crawling start...".center(62, "="))

    articles_index = {}

    current_article_id = start_id
    while len(articles_index) < num_articles:
        article_url = f"{SITE_URL}/{current_article_id}"
        article_filename = f"{PAGES_DIR}/{current_article_id}.html"

        response = requests.get(article_url)

        if response.status_code == 200:
            with open(article_filename, "w", encoding="utf-8") as article_file:
                article_file.write(response.text)
            articles_index[current_article_id] = article_url

        current_article_id += 1
        progress = (f"Progress: Article [{current_article_id}] | Index [{len(articles_index)}/{num_articles}] "
                    f"| Status Code: {response.status_code}")
        print(progress.ljust(62, " "))

    return articles_index


def create_result_files(articles_index):
    with open("index.txt", "w", encoding="utf-8") as index_txt:
        content = [f"{key} {articles_index[key]}" for key in articles_index.keys()]
        index_txt.write("\n".join(content))
    print("Saved the index.".center(62, "="))

    shutil.make_archive(DOWNLOADING_FILES_OUTPUT, 'zip', PAGES_DIR)
    print("Created the archive.".center(62, "="))


def create_or_remove_dir():
    if os.path.exists(PAGES_DIR):
        shutil.rmtree(PAGES_DIR)
    os.mkdir(PAGES_DIR)


if __name__ == '__main__':
    create_or_remove_dir()
    index = crawl_and_save_articles(start_id=700008, num_articles=PAGES_NUMBER)
    create_result_files(index)
