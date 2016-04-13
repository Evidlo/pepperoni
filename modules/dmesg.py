from twisted.internet import reactor, defer
from twisted.web.client import getPage
from basemodules import botmodule

#dmesg
class module_dmesg(botmodule):
	def run(self):
		self.bot.msg(self.bot.channel,'boggle...')
