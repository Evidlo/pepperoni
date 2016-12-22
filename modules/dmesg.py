from twisted.internet import reactor, defer
from twisted.web.client import getPage
from basemodules import botmodule

#dmesg
class module_dmesg(botmodule):
    def pong(self,user=None,latency=None):
        self.log.debug('Pong called with user={0}, time={1}'.format(user,latency))
        self.bot.msg(self.bot.channel, 'Round trip latency to {0}: {1}s'.format(user, latency))

    def run(self):
        self.log.debug('pinging...')
        self.bot.ping('Evidlo','fart')
        self.bot.append_ping_queue('Evidlo', self.pong)
        self.bot.msg(self.bot.channel,'boggle...')
