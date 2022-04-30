import os
from pathlib import Path
import sys

import urllib.parse as up
import psycopg2
from dotenv import load_dotenv


from Configuration import log
from database.migrations.schema import database_schema, database_drop_tables

import database.migrations.seeds as seeds

# Adds variables from the .env to os.environ
load_dotenv()

SCHEMA_FILEPATH = Path.cwd() / "database" / "migrations" / "01_schema.sql"


def insert_environmental_reading():
    sql_cmd = """"""


class Database:
    def __init__(self, db_url):
        self.db_url = db_url
        self.connection = self.get_database_connection(db_url)

    def __str__(self):
        return "I am a database connection object."

    @staticmethod
    def print_sql_command(cmd, values=None):
        print(f"\n-------------------------\nNow executing command : \n {cmd}\n")
        if values:
            print(f"Values: {values}\n")

    @staticmethod
    def get_database_connection(database_url: str) -> psycopg2.connect:
        """Creates a connection to the database and returns the connection object.
        Parameters:
            database_url: The URL for the database connection
        Returns:
            psycopg2 Connection object
        """
        up.uses_netloc.append("postgres")
        url = up.urlparse(database_url)

        return psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port,
        )

    def run_sql_command(self, cmd, values=None):
        """Executes a command for postgres, in which values are passed"""
        try:
            cursor = self.connection.cursor()
            if values:
                cursor.execute(cmd, (*values,))
            else:
                cursor.execute(cmd)
            self.print_sql_command(cmd, values)
            self.connection.commit()
            if "RETURNING" in cmd:
                return cursor.fetchone()[0]
        except Exception as e:
            log.exception(e)
        finally:
            cursor.close()

    def seed_database(self):
        # Sensors
        self.run_sql_command(seeds.sensor_seed_sql, seeds.basking_sensor_values)
        self.run_sql_command(seeds.sensor_seed_sql, seeds.warmhide_sensor_values)
        self.run_sql_command(seeds.sensor_seed_sql, seeds.coolhide_sensor_values)

        # Heaters on relays
        self.run_sql_command(seeds.heater_seed_sql, seeds.basking_heater_values)
        self.run_sql_command(seeds.heater_seed_sql, seeds.hide_heater_values)

    def run_sql_fetchall_command(self, cmd, values=None):
        """Executes a command for postgres, in which values are passed"""
        try:
            cursor = self.connection.cursor()
            if values:
                cursor.execute(cmd, (*values,))
            else:
                cursor.execute(cmd)
            self.print_sql_command(cmd, values)
            self.connection.commit()
            return cursor.fetchall()
        except Exception as e:
            log.exception(e)
        finally:
            cursor.close()

    def fetch_temperatures_for_snapshot(self, reading_id, print_data=False) -> list:
        fetch_temps_SQL = """SELECT * FROM environmental_reading 
        WHERE reading_id = %s
        ORDER BY sensor_id
        """

        data = self.run_sql_fetchall_command(fetch_temps_SQL, (reading_id,))

        if print_data:
            for d in data:
                print(
                    "\n_____________________\n"
                    "environmental_reading\n"
                    f"Primary Key:{d[0]}\n"
                    f"reading_id:{d[1]}\n"
                    f"sensor_id:{d[2]}\n"
                    f"temperature_c:{d[3]}\n"
                    f"humidity:{d[4]}\n"
                )
            if not data:
                print("Nothing was returned by fetch_temperatures_for_snapshot.")

        return data

    def fetch_heater_state(self, reading_id, print_data=False) -> list:
        fetch_temps_SQL = """SELECT * FROM heater_state 
        WHERE reading_id = %s
        ORDER BY heater_id
        """

        data = self.run_sql_fetchall_command(fetch_temps_SQL, (reading_id,))

        if print_data:
            for d in data:
                print(
                    "\n_____________________\n"
                    "environmental_reading\n"
                    f"Primary Key:{d[0]}\n"
                    f"reading_id:{d[1]}\n"
                    f"heater_id:{d[2]}\n"
                    f"turned_on:{d[3]}\n"
                )
            if not data:
                print("Nothing was returned by fetch_heater_state.")

        return data

    def insert_into_hardware_state(self) -> int:
        """Creates a new timestamp entry and ID in the database for a hardware state
        snapshot
        Returns:
            id: Integer value for the ID of the new snapshot
        """
        hardware_state_sql = """
        INSERT INTO hardware_state(date_time)
        VALUES (now()) RETURNING id;"""

        return self.run_sql_command(hardware_state_sql)

    def insert_into_environmental_reading(
        self, reading_id: int, sensor_id: int, temperature_c: int, humidity=0
    ):
        environmental_reading_sql = """
        INSERT INTO environmental_reading(reading_id, sensor_id, temperature_c, humidity)
        VALUES(%s,%s,%s,%s)"""  # noqa E:501

        return self.run_sql_command(
            environmental_reading_sql, (reading_id, sensor_id, temperature_c, humidity)
        )

    def insert_into_heater_state(self, reading_id, heater_id, turned_on):
        """Update database with current state of a single heater."""

        add_heater_state_sql = """
        INSERT INTO heater_state (reading_id, heater_id, turned_on)
        VALUES(%s,%s,%s)
        """
        return self.run_sql_command(
            add_heater_state_sql, (reading_id, heater_id, turned_on)
        )

    def create_database(self, reset_database: bool = True):
        db_commands = database_schema

        if reset_database:
            db_commands = database_drop_tables + db_commands

        try:
            cursor = self.connection.cursor()
            for command in db_commands:
                cursor.execute(command)
                self.print_sql_command(command)

            cursor.close()
            self.connection.commit()
        except Exception as e:
            log.exception(e)
