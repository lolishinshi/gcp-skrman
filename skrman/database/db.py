import os

from playhouse.db_url import connect
from playhouse.postgres_ext import PostgresqlExtDatabase

db = PostgresqlExtDatabase(os.getenv("DATABASE_URL"))
