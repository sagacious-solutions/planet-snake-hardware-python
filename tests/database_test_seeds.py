sensor_seed_sql = """INSERT INTO sensor(onewire_id, model, description)
    VALUES(%s,%s,%s) RETURNING id;"""

basking_sensor_values = ["0x00000123324", "DS18B20", "Basking Sensor"]
warmhide_sensor_values = ["0x000005973324", "DS18B20", "Warmhide Sensor"]
coolhide_sensor_values = ["0x000002474831", "DS18B20", "Coolhide Sensor"]

# Setup entries for heaters
heater_seed_sql = """INSERT INTO heater(socket_number, description)
    VALUES(%s,%s) RETURNING id;"""

basking_heater_values = [1, "Basking Lamp"]
hide_heater_values = [2, "Hide Heating Pads"]
