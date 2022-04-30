import sys
import os

from Configuration import log
from database.database import Database


def handle_parameter():
    """
    This function runs in place of the main function when parameters are
    passed in at the command line. Current available list of parameter
    commands are.

        - reset_db : This drops all tables from the database and recreates them
        - seed_db : Seed database with sensor and heater values

    If you are seeing this message, you passed in an invalid parameter
    """
    param = sys.argv[1]
    db_url = os.environ["DATABASE_URL"]
    database = Database(db_url)

    if param == "reset_db":
        database.create_database(reset_database=True)
        return
    if param == "seed_db":
        database.seed_database()
        return

    print(handle_parameter.__doc__)


def main():
    log.info("Main Process Ran")


if __name__ == "__main__":
    try:
        # If a parameter is passed, handle it
        if len(sys.argv) > 1:
            handle_parameter()
        else:
            main()

    except Exception as e:
        print(e)
