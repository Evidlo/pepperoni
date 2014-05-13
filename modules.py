from random import choice
from twisted.internet import reactor

class shesaid(object):
	def __init__(self,quotesFile,triggers,rate):
		self.enabled = True
		self.rate = rate
		self.triggers = triggers.split('\n')
		with open(quotesFile) as quotesFileObj:
			self.quotes = quotesFileObj.readlines()

	def run(self,user,msg):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		return choice(self.quotes)

	def enable(self):
		self.enabled = True
