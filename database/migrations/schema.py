database_schema = [
  "DROP TABLE IF EXISTS hardware_state CASCADE;",
  "DROP TABLE IF EXISTS environmental_reading CASCADE;",
  "DROP TABLE IF EXISTS heater_state CASCADE;",
  "DROP TABLE IF EXISTS heater CASCADE;",
  "DROP TABLE IF EXISTS sensor CASCADE;",


  """CREATE TABLE hardware_state(
    id SERIAL PRIMARY KEY,
    date_time TIMESTAMP NOT NULL DEFAULT Now()
  );""",

  """CREATE TABLE sensor (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(255) NOT NULL,
    sensor_model VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    date_added TIMESTAMP NOT NULL DEFAULT Now()
  );""",

  """
  CREATE TABLE environmental_reading (
    id SERIAL PRIMARY KEY,
    reading_id INTEGER REFERENCES hardware_state(id) ON DELETE CASCADE,
    sensor_id INTEGER REFERENCES sensor(id) ON DELETE CASCADE,
    temperature_c SMALLINT NOT NULL,
    humidity SMALLINT DEFAULT 0
  );
  """,
  """CREATE TABLE heater (
    id SERIAL PRIMARY KEY,
    socket_number SMALLINT NOT NULL,
    description VARCHAR(255) NOT NULL,
    date_added TIMESTAMP NOT NULL DEFAULT Now()
  );""",
  """CREATE TABLE heater_state (
    id SERIAL PRIMARY KEY,
    reading_id INTEGER REFERENCES hardware_state(id) ON DELETE CASCADE,
    heater_id INTEGER REFERENCES heater(id) ON DELETE CASCADE,
    turned_on BOOLEAN NOT NULL
  );
  """,
]
