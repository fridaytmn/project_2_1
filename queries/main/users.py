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

@query(connector)
def get_active_staff():
    """Запрос возвращает список активных сотрудников"""
    return """
    SELECT username, email, date_joined
    FROM users_user
    WHERE is_active = TRUE AND is_staff = TRUE"""

@query(connector)
def get_last_actions():
    """Возвращает последние действия пользователя"""
    return """
    SELECT u.username, l.action_time, l.object_repr
    FROM django_admin_log l
    LEFT JOIN users_user u ON l.user_id = u.id
    ORDER BY l.action_time DESC
    LIMIT 50"""

@query(connector)
def get_users_offline_6_month():
    """Возвращает пользователей, которые не заходили полгода"""
    return """
    SELECT username, last_login
    FROM users_user
    WHERE last_login < NOW() - INTERVAL '6 months'
    ORDER BY last_login ASC"""

