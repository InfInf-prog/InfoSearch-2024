## Основы информационного поиска

Выполнили студенты группы 11-001:
* Кадырова Элина
* Савинчева Ангелина

### Инструкция к запуску:
```
pip install -r requirements.txt
python3 task_*.py
```

### Задание 1
1. Архив с выкаченными страницами: [выкачка.zip](выкачка.zip)
2. Индекс: [index.txt](index.txt)

### Задание 2
1. Файл со списком токенов: [tokens.txt](tokens.txt)
2. Файл по списком лемматизированных токенов: [lemma_tokens.txt](lemma_tokens.txt)

### Задание 3
1. Файл с инвертированным индексом: [inverted_index.json](inverted_index.json)

* Код построения индекса: [task_3_index.py](task_3_index.py)
* Код реализации булев поиска: [task_3_search.py](task_3_search.py)

#### Операторы:
* AND - `&`
* OR - `|`
* NOT - `~`

#### Пример запроса:
* `(человек & код) | ~компьютер`

### Задание 4
1. Директория с файлами со списком терминов (токенов) и подсчитанными tf-idf: [tokens_tfidf](tokens_tfidf)
2. Директория с файлами по списком лемматизированных форм и подсчитанными tf-idf: [lemmas_tfidf](lemmas_tfidf)
