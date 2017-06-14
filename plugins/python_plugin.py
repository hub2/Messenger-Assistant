import io
from contextlib import redirect_stdout

from plugin_base import AbstractPluginBase


class PythonPlugin(AbstractPluginBase):
    def check_pattern(self, message):
        if message.startswith("py:"):
            return True
        else:
            return False

    def handle_message(self, message):
        command = message.split("py:", 1)[1].strip()
        output = ""
        with io.StringIO() as buf, redirect_stdout(buf):
            try:
                exec(command, {}, {})
                output = buf.getvalue()
            except Exception as e:
                output = str(e)
        return output
