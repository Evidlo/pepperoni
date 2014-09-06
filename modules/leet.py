from twisted.internet import reactor, defer
from twisted.web.client import getPage
from basemodules import botmodule

#convert text to 1337
class module_leet(botmodule):
	def init(self):
		self.leet = {'a':'4','b':'8','c':'(','d':')','e':'3','g':'6','h':'#','i':'1','l':'|','o':'0','s':'5','t':'7','w':'vv','4':'a','8':'b','(':'c',')':'d','3':'e','6':'g','#':'h','1':'i','|':'l','0':'o','5':'s','7':'t','vv':'w'}

	def run(self):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		chat = ' '.join(self.bot.chat.split(' ')[1:])
		chat = chat.lower()
		message = '' 
		for letter in chat:
			try:
				message += self.leet[letter]
			except:
				message += letter
		if message:
			self.bot.msg(self.bot.channel,message)
