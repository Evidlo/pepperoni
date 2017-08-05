from twisted.internet import reactor, defer
from twisted.web.client import getPage
import json
from basemodules import botmodule

#urban dictionary definition grabber
class module_poodict(botmodule):
    def results(self,json):
            self.log.info('Retrieving from udict')
            self.log.info(json)
            try:
                    definition = json['list'][0]['definition']
                    # truncate message to first period after 75 chars
                    message = ':: ' + definition[:75] + definition[75:].split('.')[0]
                    self.bot.msg(self.bot.channel,message)
            except KeyError:
                    self.log.info('Definition not found')
                    self.bot.msg(self.bot.channel,'nope')
    def run(self):
            args=self.bot.chat.split(' ')
            if len(args) >= 2:
                    word='%20'.join(args[1:])
                    url = "http://api.urbandictionary.com/v0/define?term="+word
                    self.log.info(url)
                    json = json.load(urllib.urlopen(url))
                    getPage(url).addCallback(json.loads).addCallback(self.results)
