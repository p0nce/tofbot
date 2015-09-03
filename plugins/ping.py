# This file is part of tofbot, a friendly IRC bot.
# You may redistribute it under the Simplified BSD License.
# If we meet some day, and you think this stuff is worth it,
# you can buy us a beer in return.
#
# Copyright (c) 2011,2015 Christophe-Marie Duquesne <chmd@chmd.fr>
#                   Martin Kirchgessner <martin.kirch@gmail.com>

"See PluginPing"
from toflib import Plugin, cmd
from datetime import datetime


class PluginPing(Plugin):

    def __init__(self, bot):
        super(PluginPing, self).__init__(bot)
        self.pings = {}

    def handle_msg(self, msg_text, _chan, nick):
        self.pings[nick] = datetime.now()

    @cmd(1)
    def cmd_ping(self, chan, args, sender_nick):
        "Find when X was last online"
        who = args[0]
        if who in self.pings:
            self.say(
                "Last message from %s was on %s (btw my local time is %s)" %
                (who, self.pings[who].__str__(), datetime.now().__str__())
            )
        else:
            self.say("I havn't seen any message from " + who)

