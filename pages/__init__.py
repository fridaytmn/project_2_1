from typing import List

import pandas as pd

from utils.page import create_pages_provider
from utils.category import create_categories_provider
import pymorphy2
from whoosh.fields import ID, Schema, TEXT, KEYWORD
from whoosh.filedb.filestore import RamStorage
from whoosh.writing import AsyncWriter
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import MultifieldParser

DATE_FORMAT_SHORT = "%Y-%m-%d"
DATE_FORMAT_SHORT_GROUP_BY_MONTH = "%Y-%m"
DATE_FORMAT_FOR_DATEPICKER = "DD-MM-YYYY"
DATE_FORMAT_SHORT_GROUP_BY_MONTH_FOR_POSTGRES = "YYYY-MM"
DATE_FORMAT_FULL = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT_FOR_CELERY = "%d-%m-%Y %H:%M"  # Дата для отображения в поле статуса отчета полученного из селери
DATE_FORMAT_BAR = "%b-%Y"
DATEPICKER_FIRST_DAY_WEEK_MONDAY = 1
DATEPICKER_CALENDAR_ORIENTATION_VERTICAL = "vertical"
DATEPICKER_NIGHT_COUNT_MIN = 0
CACHE_KEY_SCHEDULER = "scheduler."
GRAPH_CONFIG = {"doubleClickDelay": 1000}
OPTION_ALL = "все"
OPTION_YES = "да"
OPTION_NO = "нет"
SELECT_OPTIONS_LABEL_ALL = "все"
SELECT_OPTIONS_LABEL_DESKTOP = "десктопная версия"
SELECT_OPTIONS_LABEL_DESKTOP_AND_MOBILE = "десктопная и мобильная версия"
SELECT_OPTIONS_LABEL_MOBILE = "мобильная версия"
SELECT_OPTIONS_LABEL_APP = "приложение"
MAX_ALLOWABLE_CONVERSION_VALUE = 100
TABLE_DATA_STYLE = {
    "whiteSpace": "normal",
    "height": "auto",
}
TABLE_CELL_STYLE = {"maxWidth": "250px", "minWidth": "100px"}
ENTITY_TYPE_LABEL_LEGAL = "юр"  # тип субъекта правовых отношений "юридическое лицо", вариант на русском
ENTITY_TYPE_LABEL_PHYSICAL = "физ"  # тип субъекта правовых отношений "физическое лицо", вариант на русском
ENTITY_TYPE_LABEL_OTHER = "другой"  # неопределенный тип субъекта правовых отношений, вариант на русском
ENTITY_TYPE_LABEL_ALL = "все"  # все типы субъекта правовых отношений, вариант на русском
ENTITY_TYPE_LEGAL = "legal"  # тип субъекта правовых отношений "юридическое лицо", вариант на английском
ENTITY_TYPE_INDIVIDUAL = "individual"  # тип субъекта правовых отношений "физическое лицо", вариант на английском
SOURCE_FROM_MARKETPLACE = "marketplace"
ENTITY_TYPE_OTHER = "other"  # неопределенный тип субъекта правовых отношений, вариант на английском
ENTITY_TYPE_ALL = "all"  # все типы субъекта правовых отношений, вариант на английском
EMPTY_DATAFRAME = pd.DataFrame()  # Пустой датафрейм
SETTLEMENT_ID_ALL = "all"  # все id поселений
DAY_OFFSET_365 = 365  # временной период в днях
DAY_OFFSET_180 = 180  # временной период в днях
DAY_OFFSET_90 = 90  # временной период в днях
SELECT_LABEL_USER_TYPE_PAYING = "платящий"
SELECT_LABEL_USER_TYPE_NON_PAYING = "неплатящий"
USER_TYPE_PAYING = "is_payer == True"  # пользователь совершивший покупку
USER_TYPE_NON_PAYING = "is_payer == False"  # пользователь не совершавший покупку
USER_TYPE_PAYING_OR_NON_PAYING = "is_payer in [True, False]"  # любой пользователь, вне зависимости от покупки
SELECT_OPTIONS_WAREHOUSES_ALL = 2  # значение при выборе всех складов
SELECT_OPTIONS_WAREHOUSES_REMOTE = 1  # значение при выборе удаленных складов
SELECT_OPTIONS_WAREHOUSES_NON_REMOTE = 0  # значение при выборе неудаленных складов
SELECT_OPTIONS_SHOW_UNVISITED_URLS = 1  # значение при выборе параметра Показывать непосещенные URL - да
SELECT_OPTIONS_DONT_SHOW_UNVISITED_URLS = 0  # значение при выборе параметра Показывать непосещенные URL - нет
REGIONS_ALL = "all"  # выбор всех регионов, английский вариант
EMPTY_ROW = ""  # пустая строка
QUERIES_LABEL_ZERO_AND_PARTIAL_SUGGESTION = "нулевые + неточный"  # нулевые поисковые запросы и неточный поиск на сайте
QUERIES_LABEL_ZERO = "нулевые запросы"  # нулевые поисковые запросы на сайте
QUERIES_LABEL_PARTIAL_SUGGESTION = "неточный поиск"  # неточный поиск на сайте

pages_provider = create_pages_provider("./pages")
categories_provider = create_categories_provider("./pages")

morph = pymorphy2.MorphAnalyzer()


def stem(word):
    return morph.parse(word)[0].normal_form


schema = Schema(
    id=ID(stored=True),
    label=TEXT(analyzer=StemmingAnalyzer(stemfn=stem), field_boost=2.0, sortable=True),
    tags=KEYWORD(lowercase=True, analyzer=StemmingAnalyzer(stemfn=stem), field_boost=0.5),
)
storage = RamStorage()
index = storage.create_index(schema)
writer = AsyncWriter(index)

for page in pages_provider:
    writer.add_document(id=page.get_id(), label=page.get_label(), tags=[tag.value for tag in page.get_tags()])

writer.commit()


def search(search_string: str, sort_field: str | None = None) -> List[str]:
    """
    Looking compare for a match to the keywords in searching string with field's value,
    Parameters:
            search_string (str): keywords for searching
            sort_field (str or None): sort search result by this field.
                        If None search results sorts higher scores before lower scores
    Returns: the lists of founded pages id
    """
    parser = MultifieldParser(["label", "tags"], schema=schema)
    founded_ids = []
    query = parser.parse(search_string)
    with index.searcher() as s:
        results = s.search(query, limit=None, sortedby=sort_field)
        for result in results:
            founded_ids.append(result["id"])

    return founded_ids
