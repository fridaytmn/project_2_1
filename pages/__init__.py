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


TABLE_DATA_STYLE = {
    "whiteSpace": "normal",
    "height": "auto",
}
TABLE_CELL_STYLE = {"maxWidth": "250px", "minWidth": "100px"}
EMPTY_DATAFRAME = pd.DataFrame()  # Пустой датафрейм

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
    writer.add_document(id=page.get_id(), label=page.get_label())

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
