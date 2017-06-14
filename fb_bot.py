#!/usr/bin/env python3
import getpass
import sys

import fbchat
import fuckit

from plugin_base import PluginLoader


class MessengerBot(fbchat.Client):
    def __init__(self, email, password, debug=False, user_agent=None, plugins=None):
        fbchat.Client.__init__(self, email, password, debug, user_agent)
        self.plugins = plugins
        self.debug = debug

    def on_message(self, mid, author_id, author_name, message, metadata):
        print("%s said: %s" % (author_id, message))

        # Commands can be only executed by the owner
        if str(author_id) == str(self.uid):
            mate_id = metadata['delta']['messageMetadata']['threadKey'].get('otherUserFbId')
            thread_id = metadata['delta']['messageMetadata']['threadKey'].get('threadFbId')

            send_id = thread_id or mate_id
            is_user = thread_id is None

            for plugin in self.plugins:
                name, plugin_inst = plugin
                if plugin_inst.check_pattern(message):
                    if self.debug or True:
                        print("%s is handling the message" % name)
                    output = plugin_inst.handle_message(message)
                    self.send(send_id, output, is_user=is_user)


def main():
    if len(sys.argv) != 2:
        print("usage: ./fb_bot.py username")
        sys.exit(1)
    username = sys.argv[1]
    password = getpass.getpass(prompt='Facebook password: ')

    plugins = PluginLoader.get_all_plugins()
    while True:
        with fuckit:
            print("Initializing the bot")
            bot = MessengerBot(username, password, plugins=plugins)
            print("Listening...")
            bot.listen()


if __name__ == '__main__':
    main()
