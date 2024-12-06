from utils.sql import join_int, join_str
from unittest import TestCase


class TestModuleSql(TestCase):
    """Test for sql.py"""

    def test_join_int(self):
        self.assertEqual(join_int([1, 2, 3, 4, 5]), "1,2,3,4,5")
        self.assertEqual(join_int(["as", 2, "2"]), "as,2,2")
        self.assertEqual(join_int([1.2, "bb", " "]), "1.2,bb, ")
        self.assertEqual(join_int(["level", "up", "next"]), "level,up,next")
        self.assertEqual(join_int([]), "")

    def test_join_str(self):
        self.assertEqual(join_str([1, 2, 3, 4]), "'1','2','3','4'")
        self.assertEqual(join_str(["let", 78, "str"]), "'let','78','str'")
        self.assertEqual(join_str([0.56, "23", 33, "Moscow"]), "'0.56','23','33','Moscow'")
