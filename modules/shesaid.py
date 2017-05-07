from twisted.internet import reactor, defer
from twisted.web.client import getPage
from random import choice
from basemodules import botmodule

# responds to "that's what she said" in chat with a quote by a woman
class module_shesaid(botmodule):
	def init(self):
		quotesFile = 'quotes.txt'
		with open(quotesFile) as quotesFileObj:
			self.quotes = quotesFileObj.readlines()

	def run(self):
		self.bot.msg(self.bot.channel,choice(self.quotes))
