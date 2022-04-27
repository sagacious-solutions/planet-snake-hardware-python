import os

from dotenv import load_dotenv
import pytest

from database.database import Database

load_dotenv()


class Test_Database:
    @pytest.fixture(scope="class", autouse=True)
    def database(self):
        db_url = os.environ["LOCAL_DATABASE_URL"]
        db = Database(db_url)
        db.create_database()
        db.seed_database()
        return db

    def test_can_create_hardware_state_entry(self, database):
        assert database.insert_into_hardware_state() == 1
