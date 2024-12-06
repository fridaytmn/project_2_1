from datetime import timedelta, datetime

import numpy as np

from pages import DATE_FORMAT_SHORT
from typing import Union, Any
from pydantic.typing import Annotated
from pydantic import Field


def generate_annotated(types: Any, validation_rule: str) -> Annotated:
    return Annotated[types, Field(regex=validation_rule)]


class TypeUint32(object):
    """Класс для типа uint32 с валидацией"""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if np.uint32(value) != eval(value):
            raise TypeError("uint32 required")
        return value


def string_length_gap(minimum: int = 0, maximum: int = "") -> str:
    """Правило валидации: Строка не короче minimum и не длиннее maximum
    Parameters:
        minimum: Минимальное количество символов. По умолчанию 0
        maximum: Максимальное количество символов.
            По умолчанию пустое значение, строка будет неопределенной длины
    """
    return r"{" + f"{minimum}" + "," + f"{maximum}" + "}"


EXTENSIONS_ALLOWED = ".xlsx,.xls,.csv"  # расширения разрешенных к загрузке файлов
EXTENSIONS_EXCEL_ALLOWED = ".xlsx,.xls"  # эксель расширения разрешенных к загрузке файлов
VALIDATOR_CONFIG = {"extra": "allow"}
VALIDATION_RULE_DIGITS_WITH_SPACES = r"^\d+( \d+)*$"  # правило валидации: численная строка с разделением в один пробел
VALIDATION_RULE_DIGITS_LIMIT_LEN_WITH_SPACES = rf"^\d{string_length_gap(1, 25)}+( \d{string_length_gap(1, 25)}+)*$"
# правило валидации: численная строка длиной от 1 до 25 символов с разделением в один пробел
VALIDATION_RULE_EMPTY = r"^\s*$"  # правило валидации: пустая строка
VALIDATION_RULE_DIGIT = r"\d"  # правило валидации: содержит цифру
VALIDATION_RULE_ANY_SYMBOL = r"."  # любой символ кроме перехода на новую строку
VALIDATION_RULE_END_LINE = r"$"  # правило валидации: за выражением следует конец строки
VALIDATION_RULE_INT32 = r"((1\d{0,9}|2(0\d{8}|1[0-3]\d{7}|14[0-6]\d{6}|147[0-3]\d{5}|1474[0-7]\d{4}|14748[0-2]\d{3}|147483[0-5]\d{2}|1474836[0-3]\d|14748364[0-7])|[1-9]\d{0,8})|0|)"  # noqa E501
# правило валидации: строка с числом, подходящим для перевода в тип int32
VALIDATION_RULE_INT32_WITH_SPACES = rf"^{VALIDATION_RULE_INT32}(\s{VALIDATION_RULE_INT32})*$"
# правило валидации: строка, содержащая числа типа int32, разделенные пробелами
VALIDATION_RULE_BARCODE_IDS_STRING_OR_EMPTY = rf"{VALIDATION_RULE_DIGITS_WITH_SPACES}|{VALIDATION_RULE_EMPTY}"
# правило валидации: численная строка длиной от 1 до 25 символов с разделением в один пробел или пустая строка
VALIDATION_NOT_EMPTY_LINE = r"[\d?A-Z]|[\s?]$"  # правило валидации: строка не пустая
VALIDATION_START_WITH_SLASH = r"^\/\w*"  # правило валидации: строка начинается со слеша
VALIDATION_START_SLASH_OR_PERCENT = r"^[\/*]|[%*]"  # правило валидации: строка со слеша или процента

TYPE_ORDER_ID = generate_annotated(
    types=str | None,
    validation_rule=rf"^{VALIDATION_RULE_DIGIT}{string_length_gap(2, 8)}{VALIDATION_RULE_END_LINE}",
)  # аннотация для поля id заказа
TYPE_DIGITS_STRING_OR_EMPTY = generate_annotated(
    types=str, validation_rule=rf"{VALIDATION_RULE_DIGITS_WITH_SPACES}|{VALIDATION_RULE_EMPTY}"
)  # аннотация для поля sids товара или пустая строка
TYPE_BARCODE_IDS_STRING_OR_EMPTY = generate_annotated(
    types=str, validation_rule=VALIDATION_RULE_BARCODE_IDS_STRING_OR_EMPTY
)  # аннотация для поля barcode_ids
TYPE_BARCODE_ID = generate_annotated(
    types=str, validation_rule=rf"{VALIDATION_RULE_DIGIT}{string_length_gap(1, 25)}{VALIDATION_RULE_END_LINE}"
)  # аннотация типа barcode_id
TYPE_PROMOTION_CODE_ID = generate_annotated(
    types=str | None,
    validation_rule=rf"^{VALIDATION_RULE_DIGIT}{'{9}'}{VALIDATION_RULE_END_LINE}",
)  # аннотация для поля id акции
TYPE_SITE_SIDS = generate_annotated(
    types=str, validation_rule=rf"^{VALIDATION_RULE_INT32_WITH_SPACES}|{VALIDATION_RULE_EMPTY}$"
)  # аннотация для поля sids товара
TYPE_BANNER_ID = generate_annotated(
    types=str | None,
    validation_rule=rf"^{VALIDATION_RULE_DIGIT}{string_length_gap(1, 6)}{VALIDATION_RULE_END_LINE}",
)  # аннотация для поля id баннера
TYPE_ID_QUERY_PATTERN = generate_annotated(
    types=str,
    validation_rule=rf"^{VALIDATION_RULE_ANY_SYMBOL}{'{3,}'}{VALIDATION_RULE_END_LINE}",
)  # аннотация для поля паттерна поискового запроса
TYPE_NOT_EMPTY_LINE = generate_annotated(
    types=str, validation_rule=rf"{VALIDATION_NOT_EMPTY_LINE}"
)  # аннотация для пустого поля
TYPE_START_WITH_SLASH = generate_annotated(
    types=str, validation_rule=rf"{VALIDATION_START_WITH_SLASH}"
)  # аннотация для поля начинающего со слеша
TYPE_START_SLASH_OR_PERCENT = generate_annotated(
    types=str, validation_rule=rf"{VALIDATION_START_SLASH_OR_PERCENT}"
)  # аннотация для поля начинающего со слеша или знака процента


def between(start_date: Union[str, datetime], end_date: Union[str, datetime], period: int) -> bool:
    """
    Checks that the number of days between start_date and end_date does not exceed period.

    :param start_date:
        The minimum required date of the period.
    :param end_date:
        The maximum date of the period.
    :param period:
        The value of the period in days.
    """
    if type(start_date) is str and type(end_date) is str:
        end_date = datetime.strptime(end_date, DATE_FORMAT_SHORT)
        start_date = datetime.strptime(start_date, DATE_FORMAT_SHORT)
    if start_date > end_date:
        return False
    return (end_date - start_date) <= timedelta(days=period)
