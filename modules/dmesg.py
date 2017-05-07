from twisted.internet import reactor, defer
from twisted.web.client import getPage
from basemodules import botmodule

# simple debug test to calculate latency to user and verify peetsa is online
class module_dmesg(botmodule):
    def pong(self,user=None,latency=None):
        self.log.debug('Pong called with user={0}, time={1}'.format(user,latency))
        self.bot.msg(self.bot.channel, 'Round trip latency to {0}: {1}s'.format(user, latency))

    def run(self):
        user = self.bot.user
        self.log.debug('pinging...')
        self.bot.ping(user,'ping')
        self.bot.append_ping_queue(user, self.pong)
        self.bot.msg(self.bot.channel,'boggle...')
