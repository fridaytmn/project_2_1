from utils.connectors.query_wraper import query
from queries.main import connector


@query(connector)
def get_departments():
    return """SELECT DISTINCT name FROM public.organizations_department"""
