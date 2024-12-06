import importlib
import utils
from utils.user import User
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

    def get_allowed_groups(self) -> set:
        return getattr(self._module, "allowed_groups", {})


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


def categories_list_condition(category: Category, user: User | None = None) -> bool:
    if not category.is_hidden() and not category.get_allowed_groups():
        return True
    if user is not None:
        if (
            not category.is_hidden()
            and category.get_allowed_groups()
            and (not category.get_allowed_groups().isdisjoint(user.roles) or user.username in utils.allowed_users)
        ):
            return True
    return False
