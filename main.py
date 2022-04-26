import database.database as database


def main():
    database.create_database()


if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        print(e)
