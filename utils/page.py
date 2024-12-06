import importlib
import flask
from enum import Enum
from pathlib import Path
from dash import html
from typing import Optional, Any, NoReturn, Set, List, Callable
from utils.pages import BaseProvider, get_short_url, get_module_name
from utils.tag import Tag, TagProvider


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

    def is_full_screen(self) -> bool:
        return getattr(self._module, "is_full_screen", False)

    def get_content(self) -> Any:
        func = getattr(self._module, "get_content", lambda params: None)
        return func()

    def add_jobs(self, scheduler) -> NoReturn:
        func = getattr(self._module, "add_jobs", None)
        if callable(func):
            func(scheduler)

    def get_short_path(self) -> str:
        return self._short_path

    def is_attr_exist(self, attr_name) -> bool:
        if getattr(self._module, attr_name, False):
            return True

        return False

    def get_tags(self) -> Set[Tag]:
        return getattr(self._module, "tags", {})

    def is_hidden(self) -> bool:
        return getattr(self._module, "is_hidden", False)

    def is_archived(self) -> bool:
        return getattr(self._module, "is_archived", False)

    def has_tag(self, tag: Tag) -> bool:
        return tag in self.get_tags()

    def is_tags_hidden(self) -> bool:
        return getattr(self._module, "is_tags_hidden", False)

    def get_category_name(self) -> str:
        return self._category_name

    def get_note(self) -> Optional[str]:
        return getattr(self._module, "note", None)

    def get_subcategory_name(self) -> Optional[str]:
        return self._subcategory_name

    def get_allowed_roles(self) -> Set:
        return getattr(self._module, "allowed_roles", {})

    def is_open_in_new_tab(self) -> bool:
        return getattr(self._module, "is_open_in_new_tab", False)

    def get_external_link(self) -> str:
        return getattr(self._module, "external_link", None)

    def get_permanent_redirect(self) -> str:
        return getattr(self._module, "permanent_redirect", None)

    def get_allowed_users(self) -> str:
        return getattr(self._module, "allowed_users", [])

    @property
    def hit(self) -> int:
        return self._hit

    @hit.setter
    def hit(self, hit: int) -> NoReturn:
        self._hit = hit


class SortType(Enum):
    BY_NAME = "by_name"
    BY_HIT = "by_hit"


class PageProvider(BaseProvider[Page]):
    def get_tags(self) -> TagProvider:
        result = set()
        for page in self:
            result = result.union(page.get_tags())
        return TagProvider(result)


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


def pages_list_condition(page: Page, tag: Tag = None, ids: List[str] = ()) -> bool:
    return (
        not page.is_archived()
        and not page.is_hidden()
        and page_has_tag_condition(page, tag)
        and page_id_in_list_condition(page, ids)
    )


def pages_menu_condition(page: Page, category_name: str) -> bool:
    return (
        not page.is_archived()
        and not page.is_hidden()
        and page.get_category_name() == category_name
        and page.get_permanent_redirect() is None
    )


def pages_menu_condition_with_subcategories(page: Page, category_name: str, subcategory_name: str) -> bool:
    if pages_menu_condition(page, category_name) and page.get_subcategory_name() == subcategory_name:
        return True

    return False


def page_has_tag_condition(page: Page, tag: Tag = None) -> bool:
    if tag is None:
        return True

    if page.has_tag(tag):
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


def by_tag_name_sort_key(tag: Tag):
    return tag.value.lower()


def by_hit_sort_key(page: Page):
    return page.hit


def by_search_order_sort_key(founded_ids: List[str]) -> Callable[[Any], int]:
    """
    Sort key function for sorting by search order
        Parameters:
            founded_ids(): a list of sorted page's ids
    """
    return lambda page: founded_ids.index(page.get_id())


def generate_link(page: Page) -> dict:
    host = flask.request.host_url if flask.has_request_context() else ""
    match page:
        case page if page.is_open_in_new_tab():
            return {
                "children": [page.get_label() + " ", html.I(className="bi bi-box-arrow-up-right")],
                "href": host + page.get_short_path(),
                "className": "link",
                "target": "_blank",
            }
        case page if page.get_external_link():
            return {
                "children": [page.get_label() + " ", html.I(className="bi bi-box-arrow-up-right")],
                "href": page.get_external_link(),
                "className": "link",
                "target": "_blank",
            }
        case _:
            return {"children": page.get_label(), "href": "/" + page.get_short_path(), "className": "link"}
