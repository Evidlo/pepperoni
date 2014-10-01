from twisted.internet import reactor, defer
from twisted.web.client import getPage
from basemodules import botmodule
import simplejson

#get regular definitions from glosbe dictionary
class module_dict(botmodule):
	def results(self,json):
		definition = json['tuc'][0]['meanings'][0]['text']
		self.bot.msg(self.bot.channel,(':: ' + definition[:25]+definition[25:].split('.')[0])[:150])

	def run(self):
		definition = ''
		args=self.bot.chat.split(' ')
		if len(args) >= 2:
			url='http://glosbe.com/gapi/translate?from=eng&dest=eng&format=json&phrase=' + args[1]
			getPage(url).addCallback(simplejson.loads).addCallback(self.results)

