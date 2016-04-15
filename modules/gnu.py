from twisted.internet import reactor, defer
from twisted.web.client import getPage
from basemodules import botmodule

#xzibit dat stuff
class module_gnu(botmodule):
	def run(self):
		words = self.bot.chat.split(' ')
		if len(words) == 2:
			self.bot.msg(self.bot.channel,"I'd just like to interject for a moment. What you’re referring to as {0}, is in fact, GNU/{0}, or as I’ve recently taken to calling it, GNU plus {0}.  {0} is not an operating system unto itself, but rather another free component of a fully functioning GNU system made useful by the GNU corelibs, shell utilities and vital system components comprising a full OS as defined by POSIX.".format(words[1]))
