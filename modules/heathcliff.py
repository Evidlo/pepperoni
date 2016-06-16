from twisted.internet import reactor, defer
from twisted.web.client import getPage
from basemodules import botmodule
import urllib2

#heathcliff
class module_heathcliff(botmodule):
	def run(self):
		from lxml import etree
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0')]
		response = opener.open('http://www.gocomics.com/heathcliff')
		tree = etree.HTML(response.read())
		url = tree.xpath('//img[@class="strip"]')[0].attrib['src']
		self.bot.msg(self.bot.channel,url)
