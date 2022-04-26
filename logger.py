import logging


class SnekLogger:
    def __init__(self):
        self.console_log_level = logging.DEBUG
        self.FORMAT = "%(levelname)s-%(asctime)s %(filename)s:%(lineno)s - %(funcName)2s()\n    %(message)s \n"  # NOQA E:501

        self.console_handler = None
        self.logger = self.setup_stream_handlers()
        self.logger.propagate = False  # This stops the double logging

    def clear_existing_handlers(self):
        """Removes existing root level handlers and clears existing
        log handlers if present"""
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        if self.console_handler:
            self.logger.removeHandler(self.console_handler)
            self.console_handler = None

    def set_log_levels(
        self, console=logging.DEBUG,
    ):

        self.console_log_level = console
        self.setup_stream_handlers()

    def setup_stream_handlers(self):
        """Clears existing log handlers, creates console and file logger handlers, sets
        their formatting and log level

        - returns : the logger object
        """
        self.clear_existing_handlers()

        # create logger
        logger = logging.getLogger("snake")
        logger.setLevel(self.console_log_level)

        formatter = logging.Formatter(self.FORMAT)

        # Setup Console Handler
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(self.console_log_level)
        self.console_handler.setFormatter(formatter)
        # # add ch to logger
        logger.addHandler(self.console_handler)

        return logger
