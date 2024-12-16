import importlib
import flask
from enum import Enum
from pathlib import Path
from dash import html
from typing import Optional, Any, NoReturn, Set, List, Callable
from utils.pages import BaseProvider, get_short_url, get_module_name


class Page:
    def __init__(
        self,
        module,
        short_path: str,
        category_name,
        subcategory_name,
    ):
        self._module = module
        self._short_path = short_path
        self._category_name = category_name
        self._subcategory_name = subcategory_name
        self._hit = 0

    def get_id(self):
        return self._module.__name__

    def get_label(self) -> Optional[str]:
        return getattr(self._module, "label", self.get_short_path())

    def get_content(self) -> Any:
        func = getattr(self._module, "get_content", lambda params: None)
        return func()

    def get_short_path(self) -> str:
        return self._short_path

    def is_attr_exist(self, attr_name) -> bool:
        if getattr(self._module, attr_name, False):
            return True
        return False

    def is_hidden(self) -> bool:
        return getattr(self._module, "is_hidden", False)

    def get_category_name(self) -> str:
        return self._category_name

    def get_note(self) -> Optional[str]:
        return getattr(self._module, "note", None)

    def get_subcategory_name(self) -> Optional[str]:
        return self._subcategory_name

    def get_permanent_redirect(self) -> str:
        return getattr(self._module, "permanent_redirect", None)


class SortType(Enum):
    BY_NAME = "by_name"
    BY_HIT = "by_hit"


class PageProvider(BaseProvider[Page]):
    def get_tags(self):
        result = set()
        return result


def create_pages_provider(path) -> PageProvider:
    files = list(Path(path).rglob("*.[p][y]"))

    pages = []
    for path in files:
        if not path.name.startswith("__init__") and not path.name.endswith("_test.py"):
            page = create_page(path)
            if is_correct_page(page):
                pages.append(page)

    return PageProvider(pages)


def create_page(path: Path) -> Page:
    module = importlib.import_module(get_module_name(path))
    page = Page(
        module=module,
        short_path=get_short_url(path),
        category_name=path.parts[1],
        subcategory_name=path.parent.name,
    )
    return page


def is_correct_page(page: Page) -> bool:
    if not page.is_attr_exist("get_content") and not page.is_attr_exist("permanent_redirect"):
        return False

    return True


def pages_list_condition(page: Page, ids: List[str] = ()) -> bool:
    return not page.is_hidden() and page_id_in_list_condition(page, ids)


def pages_menu_condition(page: Page, category_name: str) -> bool:
    return not page.is_hidden() and page.get_category_name() == category_name and page.get_permanent_redirect() is None


def pages_menu_condition_with_subcategories(page: Page, category_name: str, subcategory_name: str) -> bool:
    if pages_menu_condition(page, category_name) and page.get_subcategory_name() == subcategory_name:
        return True

    return False


def page_id_in_list_condition(page: Page, ids: List[str]) -> bool:
    if ids is None:
        return True

    if page.get_id() in ids:
        return True

    return False


def by_label_sort_key(page: Page):
    return page.get_label().lower()


def generate_link(page: Page) -> dict:
    return {"children": page.get_label(), "href": "/" + page.get_short_path(), "className": "link"}
