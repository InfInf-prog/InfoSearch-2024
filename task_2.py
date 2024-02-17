import os
import re
import nltk
import ssl
import pymorphy2

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')


def clean_token(token):
    return re.sub("[^а-яА-ЯёЁ]", '', token)


def extract_unique_filtered_tokens(text):
    tokens = word_tokenize(text, language='russian')
    uniq_filtered_tokens = set()
    stop_words = set(stopwords.words('russian'))

    for token in tokens:
        cleaned = clean_token(token)
        if cleaned and cleaned not in stop_words and len(cleaned) > 1:
            uniq_filtered_tokens.add(cleaned)

    return uniq_filtered_tokens


def process_tokens_and_lemmas(tokens):
    analyzer = pymorphy2.MorphAnalyzer()
    lemmas = {}

    with open('tokens.txt', 'w', encoding='utf-8') as tokens_file:
        for token in tokens:
            tokens_file.write(token + '\n')
            normal_form = analyzer.parse(token)[0].normal_form

            if normal_form not in lemmas:
                lemmas[normal_form] = []
            lemmas[normal_form].append(token)

    with open('lemma_tokens.txt', 'w', encoding='utf-8') as lemma_tokens_file:
        for lemma, tokens_list in lemmas.items():
            lemma_tokens_file.write(f"{lemma} {' '.join(tokens_list)}\n")


if __name__ == "__main__":
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    text = ''
    for article in os.listdir('data/'):
        with open(os.path.join('data', article), 'r', encoding='utf-8') as file:
            text += file.read().lower() + '\n'

    unique_filtered_tokens = extract_unique_filtered_tokens(text)
    process_tokens_and_lemmas(unique_filtered_tokens)