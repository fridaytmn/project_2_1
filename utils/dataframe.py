import concurrent.futures
import io
import base64
from PIL import Image
from typing import Tuple, Optional, NoReturn, Any, Dict, Union, Sequence
import pandas as pd
from urlextract import URLExtract
import requests
from http import HTTPStatus

SPREADSHEET_LIST_NAME_LENGTH_MAX = 30  # максимальное число символов названия листа в xlsx документе

url_extractor = URLExtract(limit=1, extract_localhost=False)


def from_bytes(
    content_string: str,
    filename: str,
    dtype: Union[str, Dict] = str,
    header: int | Sequence[int] | None = None,
) -> pd.DataFrame:
    """Извлекает данные из файла в зависимости от типа файла
    Parameters:
        content_string: данные из файла
        filename: имя файла
        dtype: Тип данных для данных из файла
        header: Номера строк для использования в качестве имен столбцов и начала данных. По умолчанию None.
    Returns:
        датафрейм с данными
    """
    content_decoded = base64.b64decode(content_string)
    try:
        match filename:
            case filename if (filename.endswith("csv")):
                return pd.read_csv(
                    io.StringIO(content_decoded.decode("utf-8")), index_col=None, header=header, dtype=dtype
                )
            case filename if (filename.endswith("xlsx") or filename.endswith("xls")):
                return pd.read_excel(io.BytesIO(content_decoded), index_col=None, header=header, dtype=dtype)
            case _:
                return pd.DataFrame()
    except (ImportError, ValueError):
        return pd.DataFrame()


def convert_to_xlsx(
    data: list[list[dict]],
    sheet_names: list,
    thumbnail_column_name: str = "",
    thumbnail_size: (int, int) = (0, 0),
    is_thumbnails_enabled: bool = False,
    index: bool = True,
) -> bytes:
    with io.BytesIO() as output:
        with pd.ExcelWriter(output, "xlsxwriter") as writer:
            for row, dataframe in enumerate(data):
                dataframe = pd.DataFrame(dataframe)
                dataframe.to_excel(writer, sheet_names[row][:SPREADSHEET_LIST_NAME_LENGTH_MAX], index=index)
                if (thumbnail_column_name in dataframe.columns) and is_thumbnails_enabled:
                    thumbnail_column_index = dataframe.columns.get_loc(thumbnail_column_name) + 1
                    sheet = writer.sheets[sheet_names[row][:SPREADSHEET_LIST_NAME_LENGTH_MAX]]
                    thumbnail_urls = {
                        row_num: extract_url(value) for (row_num, value) in dataframe[thumbnail_column_name].items()
                    }
                    thumbnail(
                        sheet,
                        thumbnail_column_index,
                        thumbnail_urls,
                        thumbnail_size,
                    )
        return output.getvalue()


def thumbnail(
    sheet: Any,
    thumbnail_column_index: int,
    urls: Dict[int, str],
    thumbnail_size: Tuple[int, int],
) -> NoReturn:
    thumbnail_width, thumbnail_height = thumbnail_size
    sheet.set_column_pixels(
        first_col=thumbnail_column_index,
        last_col=thumbnail_column_index,
        width=thumbnail_width,
    )
    sheet.set_default_row(thumbnail_height)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        thumbnails = executor.map(lambda u: (u[0], get_thumbnail(u[1], thumbnail_size)), urls.items())
        [insert_thumbnail(sheet, row_num + 1, thumbnail_column_index, thumb) for row_num, thumb in thumbnails]


def extract_url(value: str) -> Optional[str]:
    if value is None:
        return None

    urls = url_extractor.find_urls(value)

    return None if len(urls) == 0 else urls.pop()


def get_thumbnail(url: str, size: Tuple[int, int]) -> io.BytesIO:
    if url is None:
        return io.BytesIO().getvalue()
    response = requests.get(url, stream=True)
    if response.status_code == HTTPStatus.NOT_FOUND.value:
        return io.BytesIO().getvalue()
    img = Image.open(response.raw)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.thumbnail(size, resample=Image.NEAREST)

    output = io.BytesIO()
    img.save(output, format="JPEG")

    return output


def insert_thumbnail(sheet: Any, row: int, col: int, image: io.BytesIO) -> NoReturn:
    sheet.insert_image(
        row,
        col,
        filename=str(row) + str(col),
        options={
            "image_data": image,
            "x_offset": 1,
            "y_offset": 1,
        },
    )
