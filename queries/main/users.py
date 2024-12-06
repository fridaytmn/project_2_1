from utils.connectors.query_wraper import query
from queries.main import connector


@query(connector)
def get_count_users():
    """Запрос возвращает количество зарегистрированных пользователей в системе"""
    return """SELECT username, name FROM public.users_user GROUP BY username, id"""
