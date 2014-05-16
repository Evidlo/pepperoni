from twisted.internet import reactor
from random import choice

class shesaid(object):
	def __init__(self):
		self.enabled = True
		self.rate = 10 
		triggers = "[Tt]hat'?s what she said"
		self.triggers = triggers.split('\n')
		quotesFile = 'quotes.txt'
		with open(quotesFile) as quotesFileObj:
			self.quotes = quotesFileObj.readlines()

	def run(self,user,msg):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		return choice(self.quotes)

	def enable(self):
		self.enabled = True
