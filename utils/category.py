import importlib
from pathlib import Path
from utils.pages import BaseProvider, get_module_name


class Category:
    _module = None
    _name: str
    _subcategories: list

    def __init__(self, module, name, subcategories):
        self._module = module
        self._name = name
        self._subcategories = subcategories

    def get_label(self) -> str:
        return getattr(self._module, "label", self._name)

    def get_name(self) -> str:
        return self._name

    def is_hidden(self) -> bool:
        return getattr(self._module, "is_hidden", False)

    def get_subcategories(self) -> list:
        return self._subcategories


class CategoryProvider(BaseProvider[Category]):
    pass


def create_categories_provider(path) -> CategoryProvider:
    files = list(Path(path).glob("*/*init*.py"))

    categories = []
    for path in files:
        category = create_category(path)
        categories.append(category)

    return CategoryProvider(categories)


def create_category(path: Path) -> Category:
    module = importlib.import_module(get_module_name(path))
    name = path.parent.name
    subcategories = [x.name for x in path.parent.iterdir() if x.is_dir() and x.name != "__pycache__"]

    return Category(module, name, subcategories)


def categories_list_condition(category: Category) -> bool:
    if not category.is_hidden():
        return True
    return False
