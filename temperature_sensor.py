"""This module provides temperature monitoring via DS18B20 sensor modules."""
# https://github.com/rgbkrk/ds18b20
from ds18b20 import DS18B20

from timer import Timer


class TemperatureMonitor:
    def __init__(self, address, zone, update_interval_seconds):
        self.sensor = DS18B20(address)
        self.zone = zone
        self.current_temperature
        self.timer = Timer(interval_seconds=update_interval_seconds)

    @property
    def current_temperature(self):
        if self.timer.is_past_interval():
            self.current_temperature = self.sensor.get_temperature()

        return self.current_temperature

    @current_temperature.setter
    def current_temperature(self, *args, **kwargs):
        raise ValueError("Setting this value isn't permitted.")
