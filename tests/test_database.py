import os
import random

from dotenv import load_dotenv
import pytest

from database.database import Database
import tests.database_test_seeds as seeds


load_dotenv()


class Test_Database:
    @pytest.fixture(scope="class", autouse=True)
    def database(self):
        db_url = os.environ["LOCAL_DATABASE_URL"]
        db = Database(db_url)
        db.create_database()

        # Seed test Sensors
        db.run_sql_command(seeds.sensor_seed_sql, seeds.basking_sensor_values)
        db.run_sql_command(seeds.sensor_seed_sql, seeds.warmhide_sensor_values)
        db.run_sql_command(seeds.sensor_seed_sql, seeds.coolhide_sensor_values)

        # Seed test Heaters
        db.run_sql_command(seeds.heater_seed_sql, seeds.basking_heater_values)
        db.run_sql_command(seeds.heater_seed_sql, seeds.hide_heater_values)

        return db

    def test_can_create_hardware_state_entry(self, database):
        assert database.insert_into_hardware_state() == 1

    def test_can_add_temperature_readings_to_database(self, database):

        for _ in range(10):
            state_id = database.insert_into_hardware_state()

            for s_id in range(1, 4):
                database.insert_into_environmental_reading(
                    reading_id=state_id,
                    sensor_id=s_id,
                    temperature_c=random.randint(17, 35),
                )

        database_contents = database.fetch_temperatures_for_snapshot(2, print_data=True)

        # print(database_contents)
        assert len(database_contents) == 3

    def test_can_add_heater_state_to_the_datebase(self, database):

        state_id = database.insert_into_hardware_state()
        for heater_num in range(1, 3):

            database.insert_into_heater_state(
                reading_id=state_id, heater_id=heater_num, turned_on=True
            )

        database_contets = database.fetch_heater_state(
            reading_id=state_id, print_data=True
        )

        assert len(database_contets) == 2
