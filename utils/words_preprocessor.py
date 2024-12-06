import string
from typing import List

import nltk.corpus
import pymorphy2


stop_words = nltk.corpus.stopwords.words("russian")
morph = pymorphy2.MorphAnalyzer()


def tokenize(text: str) -> List[str]:
    """Функция для токенизации текста
    Parameters:
        text: исходная текстовая строка
    Return:
        список слов из запроса, приведенных к нижнему регистру
    """
    tokens_with_punctuation = nltk.word_tokenize(text)
    tokens = [i.lower() for i in tokens_with_punctuation if (i not in string.punctuation)]
    filtered_tokens = [i for i in tokens if (i not in stop_words)]
    return filtered_tokens


def normalize(words: List[str], words_count: int = None) -> List[str]:
    """Переводит слова к нормальной форме
    Parameters:
        words: список слов
        words_count: количество слов из списка, которые нужно вернуть,
                    по умолчанию возвращается весь список
    Return:
        список нормализированных слов
    """
    words = [morph.parse(word)[0].normal_form for word in words]
    return words[:words_count]
