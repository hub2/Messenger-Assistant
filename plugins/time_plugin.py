import time

from plugin_base import AbstractPluginBase


class TimePlugin(AbstractPluginBase):
    def check_pattern(self, message):
        if message == "time":
            return True
        else:
            return False

    def handle_message(self, message):
        return time.ctime()
