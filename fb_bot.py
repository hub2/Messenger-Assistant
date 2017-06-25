#!/usr/bin/env python3
from getch import getch
import getpass
import sys
import os
from multiprocessing import Process
from threading import Thread
import fbchat
import fuckit

from plugin_base import PluginLoader


class MessengerBot(fbchat.Client):
    def __init__(self, email, password, debug=True, user_agent=None):
        fbchat.Client.__init__(self, email, password, debug, user_agent)
        self.debug = debug

    def on_message(self, mid, author_id, author_name, message, metadata):
        print("%s said: %s" % (author_id, message))

        # Commands can be only executed by the owner
        if str(author_id) == str(self.uid):
            mate_id = metadata['delta']['messageMetadata']['threadKey'].get('otherUserFbId')
            thread_id = metadata['delta']['messageMetadata']['threadKey'].get('threadFbId')

            send_id = thread_id or mate_id
            is_user = thread_id is None
            processes = []
            self.plugins = PluginLoader.get_all_plugins()
            for plugin in self.plugins:
                name, plugin_inst = plugin
                if plugin_inst.check_pattern(message):
                    if self.debug or True:
                        print("%s is handling the message" % name)
                    p = Process(target=self.work, args=(plugin_inst, send_id, message, is_user))
                    p.start()
                    processes.append(p)
                    #output = plugin_inst.handle_message(message)
                    #self.send(send_id, output, is_user=is_user)
            for p in processes:
                p.join(30)

    def work(self, plugin, send_id, message, is_user):
        output = plugin.handle_message(message)
        self.send(send_id, output, is_user=is_user)

def reload_plugins_on_demand():
    unbuff = os.fdopen(sys.stdin.fileno(), 'rb', buffering=0)
    while True:
        c = unbuff.read(1)
        if c == b"r":
            PluginLoader.reload_plugins()

def main():
    if len(sys.argv) != 2:
        print("usage: ./fb_bot.py username")
        sys.exit(1)
    username = sys.argv[1]
    password = getpass.getpass(prompt='Facebook password: ')

    print("Initializing the bot")
    print("Press r at any time to reload plugins")
    bot = MessengerBot(username, password)
    t = Thread(target=reload_plugins_on_demand)
    t.start()
    print("Listening...")
    bot.listen()


if __name__ == '__main__':
    main()
