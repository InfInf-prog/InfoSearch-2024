import json

from os import listdir
from os.path import isfile, join

from bs4 import BeautifulSoup

PAGES_DIR = 'data/'
TOKENS_FILE = open('tokens.txt', encoding='utf-8')


def build_index():
    filenames = listdir(PAGES_DIR)
    filenames.sort(key=lambda x: int(x.replace('.html', '')))

    texts = [BeautifulSoup(open(PAGES_DIR + f).read(), 'html.parser').
             get_text().lower() for f in filenames if isfile(join(PAGES_DIR, f))]

    inverted_index = {}
    for token in TOKENS_FILE.read().splitlines():
        for i, text in enumerate(texts):
            if token in text:
                if token not in inverted_index:
                    inverted_index[token] = set()
                inverted_index[token].add(filenames[i])

    for key in inverted_index.keys():
        inverted_index[key] = list(inverted_index[key])
    json_inverted_index = json.dumps(inverted_index, ensure_ascii=False)
    with open('inverted_index.json', 'w+', encoding='utf-8') as index_file:
        index_file.write(json_inverted_index)


if __name__ == "__main__":
    build_index()
