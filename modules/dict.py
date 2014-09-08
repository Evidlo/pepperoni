from twisted.internet import reactor, defer
from twisted.web.client import getPage
from basemodules import botmodule
import simplejson

#get regular definitions from glosbe dictionary
class module_dict(botmodule):
	def run(self):
		definition = ''
		word=self.bot.chat.split(' ')[1]
		url='http://glosbe.com/gapi/translate?from=eng&dest=eng&format=json&phrase=' + word
		getPage(url).addCallback(simplejson.loads).addCallback(results)

	def results(self,json)
		definition = json['tuc'][0]['meanings'][0]['text']
		self.bot.msg(self.bot.channel,':: ' + definition[0:200])
