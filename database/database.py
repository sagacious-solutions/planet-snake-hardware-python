import os
from pathlib import Path
import sys

import urllib.parse as up
import psycopg2
from dotenv import load_dotenv


from Configuration import log
from database.migrations.schema import database_schema, database_drop_tables

load_dotenv()

SCHEMA_FILEPATH = Path.cwd() / "database" / "migrations" / "01_schema.sql"

up.uses_netloc.append("postgres")
url = up.urlparse(os.environ["DATABASE_URL"])
db_connection = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port,
)


def create_database(reset_database: bool = True):
    db_commands = database_schema

    if reset_database:
        db_commands = database_drop_tables + db_commands

    try:
        cursor = db_connection.cursor()
        for command in db_commands:
            cursor.execute(command)
            print(
                f"\n-------------------------\nNow executing command : \n {command}\n"
            )

        cursor.close()
        db_connection.commit()
    except Exception as e:
        log.exception(e)


if __name__ == "__main__":
    globals()[sys.argv[1]]()
