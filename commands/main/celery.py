from utils.connectors.command_wraper import command
from queries.dash import connector


@command(connector)
def check_and_update_status(version: str) -> str:
    """Обновляет статусы у отчетов в БД которые были просрочены"""
    return f"""
        UPDATE reports_users_in_celery
        SET status = 'outdated'
        WHERE version != '{version}' AND status != 'processing';
    """


@command(connector)
def update_data(
    username: str,
    status: str,
    label: str,
    version: str,
    params: str,
    date_finished: str | None = None,
    result: str | None = None,
) -> str:
    """Обновляет значения запроса в БД по пользователю"""
    return f"""UPDATE reports_users_in_celery
        SET status = '{status}', version = '{version}',
            result = '{result}', date_finished = '{date_finished}',
            params = '{params}'
        WHERE username = '{username}' AND report_name = '{label}'"""


@command(connector)
def create_new_query(username: str, report: str, ci_commit_sha: str, params: str) -> str:
    """Создает новую запись с начальной информацией о пользователе. версии и названии отчета и параметрами"""
    return f"""INSERT INTO reports_users_in_celery (username,
    report_name,
    version,
    params,
    status)
    VALUES ('{username}', '{report}',
            '{ci_commit_sha}', '{params}',
            'processing')
"""
