import random

from plugin_base import AbstractPluginBase


class OkseniaczPlugin(AbstractPluginBase):
    def check_pattern(self, message):
        if message == "okseń_to":
            return True
        else:
            return False

    def handle_message(self, message):
        output = "Okseniłem to na %d/10" % random.randint(0, 10)
        return output
