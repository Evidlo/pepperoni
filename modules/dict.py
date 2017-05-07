from twisted.internet import reactor, defer
from twisted.web.client import getPage
from basemodules import botmodule
import simplejson

# look up definitions or translations using glosbe api
# e.g.
#   !dict foobar
#   !trans en jp hello
class module_dict(botmodule):
    def results_dictionary(self,json):
        definition = json['tuc'][0]['meanings'][0]['text']
        self.bot.msg(self.bot.channel,(':: ' + definition[:25]+definition[25:].split('.')[0])[:150])
    def results_translate(self,json):
        definition = json['tuc'][0]['phrase']['text']
        out = definition[:25]+definition[25:].split('.')[0][:150]
        self.bot.msg(self.bot.channel,(':: ' + out.encode('utf8')))

    def run(self):
        definition = ''
        args=self.bot.chat.split(' ')
        if len(args) >= 2:
            if args[0] == '!dict':
                self.log.debug('Definition lookup requested')
                url='http://glosbe.com/gapi/translate?from=eng&dest=eng&format=json&phrase=' + args[1]
                self.log.debug('Getting url: '+url)
                getPage(url).addCallback(simplejson.loads).addCallback(self.results_dictionary)
            if args[0] == '!trans':
                if len(args) >= 4:
                    self.log.debug('Translation requested')
                    from_lang = args[1]
                    to_lang = args[2]
                    phrase = args[3]
                    url='http://glosbe.com/gapi/translate?from={0}&dest={1}&format=json&phrase={2}'.format(from_lang,to_lang,phrase)
                    self.log.debug('Getting url: '+url)
                    getPage(url).addCallback(simplejson.loads).addCallback(self.results_translate)

