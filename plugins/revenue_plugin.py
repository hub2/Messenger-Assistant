import hmac
import json
import time
import urllib

import requests

from config import *
from plugin_base import AbstractPluginBase


class RevenuePlugin(AbstractPluginBase):
    def check_pattern(self, message):
        if message == "revenue":
            return True
        else:
            return False

    def handle_message(self, message):
        info = self.get_balance_info()
        if info['success'] == 0:
            return "Nie mogę pobrać danych, error: %s" % info['error']
        print(info)
        balance = info["balances"]
        etc_val = json.loads(requests.get(api_bitbay_etc_call).text)
        btc_val = json.loads(requests.get(api_bitbay_btc_call).text)
        pln = float(balance["PLN"]["available"]) + float(balance["PLN"]["locked"])
        etc = float(balance["ETH"]["available"]) + float(balance["ETH"]["locked"])
        btc = float(balance["BTC"]["available"]) + float(balance["BTC"]["locked"])
        fee = (100 - float(info["fee"])) / 100
        etc_bid = float(etc_val["bid"])
        btc_bid = float(btc_val["bid"])

        etc_in_pln = etc * fee * etc_bid
        btc_in_pln = btc * fee * btc_bid

        revenue = etc_in_pln + btc_in_pln + pln
        output = "W tym momencie wartość Twoich krypto to: %.2f (BTC: %f*%.2f = %.2fPLN ETH: %f*%.2f = %.2fPLN PLN: %.2f)" % (
            revenue, btc, btc_bid, btc_in_pln, etc, etc_bid, etc_in_pln, pln)
        return output

    def get_balance_info(self):
        post = {"method": "info", "moment": int(time.time())}
        post_data = urllib.parse.urlencode(post).encode("utf-8")

        h = hmac.new(api_bitbay_priv, post_data, digestmod="sha512")
        headers = {"API-Key": api_bitbay_pub,
                   "API-Hash": h.hexdigest()}
        r = requests.post(api_bitbay, headers=headers, data=post)
        return json.loads(r.text)

def main():
    r = RevenuePlugin()
    print(r.handle_message("revenue"))

if __name__ == '__main__':
    main()
