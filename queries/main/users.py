from utils.connectors.query_wraper import query
from queries.main import connector


@query(connector)
def get_count_users():
    """Запрос возвращает количество зарегистрированных пользователей в системе"""
    return """SELECT username, name FROM public.users_user GROUP BY username, id"""

@query(connector)
def get_last_input_superusers():
    """Запрос возвращает дату последнего входа каждого суперпользователя"""
    return """
    SELECT name, last_login
    FROM public.users_user
    WHERE is_superuser IS NOT NULL
    AND NOT name = ''
    ORDER BY name"""