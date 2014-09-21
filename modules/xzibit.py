from twisted.internet import reactor, defer
from twisted.web.client import getPage
from basemodules import botmodule

#xzibit dat stuff
class module_yodawg(botmodule):
	def run(self):
		words = self.bot.chat.split(' ')
		a = b = None
		if len(words) == 2:
			a = words[1]
			b = a
		if len(words) >= 3:
			a = words[1]
			b = words[2]
		if a and b:
			self.bot.msg(self.bot.channel,'Yo dawg, I heard you like '+a+', so we put '+a+' in your '+b+' so you can '+a+' while you '+b)
