from pathlib import PosixPath
from types import SimpleNamespace

from utils.pages import (
    get_module_name,
    get_short_url,
    BaseProvider,
)
from utils.page import (
    create_pages_provider,
    Page,
    PageProvider,
    by_tag_name_sort_key,
)
from utils.tag import Tag
from unittest import TestCase


class TestModulePages(TestCase):
    def test_create_provider(self):
        self.assertGreater(len(create_pages_provider("./pages").filter(lambda a: True)), 1)

    def test_get_module_name(self):
        self.assertEqual(
            "pages.behavior.user_actions.traffic",
            get_module_name(PosixPath("../pages/behavior/user_actions/traffic.py")),
        )
        self.assertEqual(
            "pages.index",
            get_module_name(PosixPath("./pages/index.py")),
        )
        self.assertEqual(
            "index",
            get_module_name(PosixPath("./index.py")),
        )

    def test_get_short_url(self):
        self.assertEqual(
            "behavior/traffic",
            get_short_url(PosixPath("./pages/behavior/traffic.py")),
        )
        self.assertEqual(
            "index",
            get_short_url(PosixPath("./pages/index.py")),
        )

    def test_providers(self):
        p = BaseProvider({1, 2, 3})
        self.assertEqual(1, p.one())
        self.assertEqual(2, p.filter(lambda item: item == 2).one())

        p1 = Page(
            module=SimpleNamespace(tags={Tag.CONVERSION, Tag.DESKTOP}),
            short_path="qwe/qwe1",
            category_name="conversion",
            subcategory_name="misc",
        )
        p2 = Page(
            module=SimpleNamespace(tags={Tag.ORDER, Tag.CONVERSION}),
            short_path="qwe/qwe2",
            category_name="conversion",
            subcategory_name="conversion",
        )
        provider = PageProvider({p1, p2})
        self.assertEqual(
            [Tag.CONVERSION, Tag.DESKTOP, Tag.ORDER],
            provider.get_tags().sort_natural(by_tag_name_sort_key),
        )
