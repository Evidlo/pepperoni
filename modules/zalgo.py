from twisted.internet import reactor, defer
from twisted.web.client import getPage
from basemodules import botmodule

# converts text to zalgo using table in zalgo_dict.py
class module_zalgo(botmodule):
	def init(self):
		zalgo_dict={}
		execfile('zalgo_dict.py',zalgo_dict,zalgo_dict)
		self.zalgo_dict = zalgo_dict

	def run(self):
		message = ' '.join(self.bot.chat.split(' ')[1:])
		out = [letter + choice(self.zalgo_dict['zalgo_up']) * 2 + choice(self.zalgo_dict['zalgo_down']) * 2 + choice(self.zalgo_dict['zalgo_mid']) * 2 for letter in message]
		out = out[:27]
		self.bot.msg(self.bot.channel,''.join(out).encode('utf8'))
