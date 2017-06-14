import json
from pprint import pformat

import requests

from config import *
from plugin_base import AbstractPluginBase


class EthStatsPlugin(AbstractPluginBase):
    def check_pattern(self, message):
        if message == "ethstats":
            return True
        else:
            return False

    def handle_message(self, message):
        r = requests.get(api_bitbay_etc_call)
        output = pformat(json.loads(r.text), indent=4)
        return output


class BtcStatsPlugin(AbstractPluginBase):
    def check_pattern(self, message):
        if message == "btcstats":
            return True
        else:
            return False

    def handle_message(self, message):
        r = requests.get(api_bitbay_btc_call)
        output = pformat(json.loads(r.text), indent=4)
        return output


class MinerStatsPlugin(AbstractPluginBase):
    def check_pattern(self, message):
        if message == "minerstats":
            return True
        else:
            return False

    def handle_message(self, message):
        r = requests.get(api_nanopool_call)
        output = pformat(json.loads(r.text), indent=4)
        return output
