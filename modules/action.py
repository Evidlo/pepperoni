from twisted.internet import reactor, defer
from twisted.web.client import getPage
from basemodules import botmodule

#responds to actions
class module_action(botmodule):
	def run(self):
		try:
			message = self.bot.chat.split(' ')[0]+' '+self.bot.user
			self.bot.msg(self.bot.channel,'\001ACTION %s\001' % message)
		except IndexError:
			pass
