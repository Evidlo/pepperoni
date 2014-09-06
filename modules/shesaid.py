from twisted.internet import reactor, defer
from twisted.web.client import getPage
from random import choice
from botmodule import botmodule
	
#spouts a quote by a women as a quip to 'thats what she said'
class module_shesaid(botmodule):
	def init(self):
		quotesFile = 'quotes.txt'
		with open(quotesFile) as quotesFileObj:
			self.quotes = quotesFileObj.readlines()

	def run(self):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		self.bot.msg(self.bot.channel,choice(self.quotes))
