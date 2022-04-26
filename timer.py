from datetime import datetime, timedelta


class Timer:
    def __init__(self, interval_seconds: int = 60):
        self.interval_seconds = interval_seconds
        self.last_tick = None

    def is_past_interval(self):
        if not self.last_tick or self.last_tick > datetime.now() + timedelta(
            seconds=self.interval_seconds
        ):
            self._reset_interval_timer()
            return True

        return False

    def _reset_interval_timer(self):
        self.last_tick = datetime.now()
