import os
from pathlib import Path
import sys

import urllib.parse as up
import psycopg2
from dotenv import load_dotenv


from Configuration import log
from database.migrations.schema import database_schema, database_drop_tables

import database.migrations.seeds as seeds

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
            _print_sql_command(command)

        cursor.close()
        db_connection.commit()
    except Exception as e:
        log.exception(e)


def _print_sql_command(cmd, values=None):
    print(f"\n-------------------------\nNow executing command : \n {cmd}\n")
    if values:
        print(f"Values: {values}\n")


def _run_command(cmd, values=None):
    """Executes a command for postgres, in which values are passed"""
    try:
        cursor = db_connection.cursor()
        cursor.execute(cmd, (*values,))
        _print_sql_command(cmd, values)
        cursor.close()
        db_connection.commit()
    except Exception as e:
        log.exception(e)


def seed_database():
    # Sensors
    _run_command(seeds.sensor_seed_sql, seeds.basking_sensor_values)
    _run_command(seeds.sensor_seed_sql, seeds.warmhide_sensor_values)
    _run_command(seeds.sensor_seed_sql, seeds.coolhide_sensor_values)

    # Heaters on relays
    _run_command(seeds.heater_seed_sql, seeds.basking_heater_values)
    _run_command(seeds.heater_seed_sql, seeds.hide_heater_values)
