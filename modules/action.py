from twisted.internet import reactor, defer
from twisted.web.client import getPage

#responds to actions
class module_action(botmodule):
	def run(self):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		try:
			message = self.bot.chat.split(' ')[0]+' '+self.bot.user
			self.bot.msg(self.bot.channel,'\001ACTION %s\001' % message)
		except IndexError:
			pass
