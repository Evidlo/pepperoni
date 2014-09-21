from twisted.internet import reactor, defer
from twisted.web.client import getPage
import simplejson
from basemodules import botmodule

#urban dictionary definition grabber
class module_poodict(botmodule):
	def run(self):
		args='%20'.join(self.bot.chat.split(' '))
		if len(args) >= 2:
			word = args[1:]
			url = "http://api.urbandictionary.com/v0/define?term="+word
			json = simplejson.load(urllib.urlopen(url))
			getPage(url).addCallback(simplejson.loads).addCallback(results)

	def results(self,json):
		try:
			definition = json['list'][0]['definition']
			message = ':: ' + definition.split('.')[0]
			self.bot.msg(self.bot.channel,message)
		except KeyError:
			self.log.info('Definition not found')
