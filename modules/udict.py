from twisted.internet import reactor, defer
from twisted.web.client import getPage
import simplejson
from basemodules import botmodule

#urban dictionary definition grabber
class module_poodict(botmodule):
	def run(self):
		word='%20'.join(self.bot.chat.split(' ')[1:])
		url = "http://api.urbandictionary.com/v0/define?term="+word
		json = simplejson.load(urllib.urlopen(url))
		getPage(url).addCallback(simplejson.loads).addCallback(results)

	def results(self,json):
		definition = json['list'][0]['definition']
		message = ':: ' + definition[0:200]
		self.bot.msg(self.bot.channel,message)
