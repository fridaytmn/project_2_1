from queries.dash.celery import get_result_for_report
import pandas as pd
import json

username = "shvets_vv"
label = "pages.dev.dev_celery"

# def get_result(username: str, label: str) -> pd.DataFrame:
#     """Получить результат из БД"""
#     res = []
#     results = get_result_for_report(username, label).result[0]
#     for result in json.loads(results):
#         res_1 = json.loads(result)
#         res_2 = pd.DataFrame.from_dict(res_1)
#         res.append(res_2)
#     return res
#
# def get_result(username: str, label: str) -> list[pd.DataFrame]:
#     """Получить результат из БД"""
#     res = []
#     results = get_result_for_report(username, label).result[0]
#     for result in json.loads(results):
#         res.append(pd.DataFrame.from_dict(json.loads(result)))
#     return res
#
# print(get_result(username, label))

articles_data = traffic_data = pd.DataFrame()

print(type(articles_data), type(traffic_data))