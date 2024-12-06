import os
from utils.connectors.postgres import PostgreSQL

ENV_PREFIX = "MAIN_DB"
connector = PostgreSQL(
    host=os.environ.get(ENV_PREFIX + "_HOST", "localhost"),
    user=os.environ.get(ENV_PREFIX + "_USERNAME", "postgres"),
    port=os.environ.get(ENV_PREFIX + "_PORT", 5432),
    password=os.environ.get(ENV_PREFIX + "_PASSWORD", "postgres"),
    database=os.environ.get(ENV_PREFIX + "_NAME", "postgres"),
)
