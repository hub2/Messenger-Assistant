#!/usr/bin/env python3
import fbchat
import getpass
import time
import shutil
from pprint import pformat
import json
import random
#subclass fbchat.Client and override required methods
import sys
import contextlib
import io
from contextlib import redirect_stdout, redirect_stderr
import requests
import hmac
import urllib
from config import *
 
class EchoBot(fbchat.Client):
 
    def __init__(self,email, password, debug=True, user_agent=None):
        fbchat.Client.__init__(self,email, password, debug, user_agent)
 
    def on_message(self, mid, author_id, author_name, message, metadata):
        #self.markAsDelivered(author_id, mid) #mark delivered
        #self.markAsRead(author_id) #mark read
        print ("---- ", metadata, "------")
        print("%s said: %s"%(author_id, message))
        #if you are not the author, echo
        if str(author_id) == str(self.uid):
            mate_id = metadata['delta']['messageMetadata']['threadKey'].get('otherUserFbId')
            thread_id = metadata['delta']['messageMetadata']['threadKey'].get('threadFbId')
            is_user=True
            if thread_id is not None:
                send_id = thread_id
                is_user = False
            else:
                send_id = mate_id
 
            if message.startswith("python:"):
                command = message.split("python:", 1)[1].strip()
                if "bierz go" in command:
                    output = random.choice(["Tak jest Hubercik, juz go wpierdalam", "Zara go opierdole na ciepło", "Tego grubasa? Nie pomieszczę w brzuchu", "Jestem tylko malym wenżem, nic nie zrobię :(", "Lubię jeść placki!", "E, gruby, odpierdol sie od Hubercika, dobrze?"])
                else:
                    output = ""
                    with io.StringIO() as buf, redirect_stdout(buf):
                        try:
                            exec(command, {}, {})
                            output = buf.getvalue()
                        except Exception as e:
                            output = str(e)
            elif message == "ethstats":
                r = requests.get(api_bitbay_etc_call)
                output = pformat(json.loads(r.text), indent=4)
            elif message == "btcstats":
                r = requests.get(api_bitbay_btc_call)
                output = pformat(json.loads(r.text), indent=4)
            elif message == "minerstats":
                r = requests.get(api_nanopool_call)
                output = pformat(json.loads(r.text), indent=4)
            elif message == "weather":
                self.sendRemoteImage(send_id, message="", image=api_weather_call, is_user=is_user)
                return
            elif message == "triggered":
                self.sendRemoteImage(send_id, message="", image=api_triggered_call, is_user=is_user)
                return
            elif message == "time":
                output = time.ctime()
            elif message == "howmuch?":
                info = get_balance_info()
                print(info)
                balance = info["balances"]
                etc_val = json.loads(requests.get(api_bitbay_etc_call).text)
                btc_val = json.loads(requests.get(api_bitbay_btc_call).text)
                etc = float(balance["ETH"]["available"]) + float(balance["ETH"]["locked"])
                btc = float(balance["BTC"]["available"]) + float(balance["BTC"]["locked"])
                fee = (100 - float(info["fee"]))/100
                etc_bid = float(etc_val["bid"])
                btc_bid = float(btc_val["bid"])

                etc_in_pln = etc*fee*etc_bid
                btc_in_pln = btc*fee*btc_bid

                revenue = etc_in_pln + btc_in_pln
                output = "W tym momencie wartość Twoich krypto to: %.2f (BTC: %f*%.2f = %.2fPLN ETH: %f*%.2f = %.2fPLN)" % (revenue, btc, btc_bid, btc_in_pln, etc, etc_bid, etc_in_pln)
            elif message == "okseń_to":
                output = "Okseniłem to na %d/10" % random.randint(0, 10)
            else:
                return
            self.send(send_id, output,is_user=is_user)

def get_balance_info():
    post = {"method":"info", "moment":int(time.time())}
    post_data = urllib.parse.urlencode(post).encode("utf-8")

    h = hmac.new(api_bitbay_priv, post_data, digestmod="sha512")
    headers = {"API-Key":api_bitbay_pub,
               "API-Hash":h.hexdigest()}
    r = requests.post(api_bitbay, headers=headers, data=post)
    return json.loads(r.text)




def main():
    if len(sys.argv) != 2:
        print ("usage: ./fb_bot.py username")
        sys.exit(1)
    username = sys.argv[1]
    password = getpass.getpass(prompt='Facebook password: ')

    bot = EchoBot(username, password)
    bot.listen()


if __name__ == '__main__':
    main()
