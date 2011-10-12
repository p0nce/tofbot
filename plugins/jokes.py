from tofdata.jokes import jokes
from tofdata.chucknorris import chuckNorrisFacts
from tofdata.riddles import riddles
from tofdata.tofades import tofades
from tofdata.fortunes import fortunes
from tofdata.contrepetries import contrepetries
from toflib import cmd, InnocentHand, RiddleTeller, Plugin
import random
import time

class PluginJokes(Plugin):

    def __init__ (self, bot):
        Plugin.__init__(self, bot)
        self._jokes = InnocentHand(jokes)
        self._chuck = InnocentHand(chuckNorrisFacts)
        self._tofades = InnocentHand(tofades)
        self._riddles = InnocentHand(riddles)
        self._fortunes = InnocentHand(fortunes)
        self._contrepetries = InnocentHand(contrepetries)
        bot._mutable_attributes["autoTofadeThreshold"] = int
        bot._mutable_attributes["riddleMaxDist"] = int

    @cmd(0)
    def cmd_blague(self, chan, args):
        self.say(self._jokes())

    @cmd(0)
    def cmd_fortune(self, chan, args):
        self.say(self._fortunes())

    @cmd(0)
    def cmd_chuck(self, chan, args):
        self.say(self._chuck())

    @cmd(0)
    def cmd_tofade(self, chan, args):
        self.say(self._tofades())
            
    @cmd(0)
    def cmd_contrepetrie(self, chan, args):
        self.say(self._contrepetries())

    @cmd(1)
    def cmd_tofme(self, chan, args):
        who = args[0]
        self.say("%s : %s" % (who, self._tofades()))

    @cmd(0)
    def cmd_devinette(self, chan, args):
        if not self.active_riddle():
            self.devinette = self.random_riddle(chan)

    def handle_join(self, chan, nick):
        if nick == self.bot.nick:
            self.cmd_tofade(chan, [])
        else:
            self.cmd_tofme(chan, [nick])
        
    def handle_msg(self, msg_text, chan, nick):
        if self.active_riddle():
            itsOver = self.devinette.wait_answer(chan, msg_text)
            if itsOver:
                self.devinette = None

        if (random.randint(0, 100) > self.bot.autoTofadeThreshold and 
            (time.time() - self.bot.lastTGtofbot) >= (self.bot.TGtime * 60)):
            self.cmd_tofme(chan, [nick])


    def active_riddle(self):
        return (hasattr(self, 'devinette') and self.devinette is not None)
    
    def random_riddle(self, chan):
        riddle = self._riddles()
        r = RiddleTeller (riddle,
                          chan,
                          self.say,
                          self.bot.riddleMaxDist)
        return r

